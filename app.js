(function () {
  "use strict";
  var DATA = window.CFP_DATA;
  var COLORS = { fsu: "#782f40", iu: "#990000", psu: "#1e407c" };
  var state = { prog: "fsu", ver: {}, q: "" };

  try {
    var saved = localStorage.getItem("cfp.prog");
    if (saved && DATA.programs.some(function (p) { return p.id === saved; })) state.prog = saved;
  } catch (e) { /* storage unavailable */ }
  if (location.hash) {
    var h = location.hash.slice(1);
    if (DATA.programs.some(function (p) { return p.id === h; })) state.prog = h;
  }

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "text") n.textContent = attrs[k];
      else if (k === "class") n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function link(label, url, cls) {
    return el("a", { href: url, target: "_blank", rel: "noopener noreferrer", class: cls || "", text: label });
  }
  function prog() { return DATA.programs.find(function (p) { return p.id === state.prog; }); }
  function version(p) {
    var id = state.ver[p.id] || p.versions[0].id;
    return p.versions.find(function (v) { return v.id === id; }) || p.versions[0];
  }
  function matches(c) {
    if (!state.q) return true;
    var names = (c.instructors && c.instructors.history || []).map(function (r) { return r.names.join(" "); }).join(" ");
    var hay = [c.code, c.title, c.descEn, c.descKo, c.note, names].join(" ").toLowerCase();
    return state.q.toLowerCase().split(/\s+/).every(function (t) { return hay.indexOf(t) !== -1; });
  }


  // ---- professor index: name -> programs/courses/terms (only from verified records)
  var TERM_RANK = { Spring: 1, Summer: 2, Fall: 3 };
  function termKey(t) {
    var m = /(Spring|Summer|Fall)\s+(\d{4})/.exec(t);
    return m ? parseInt(m[2], 10) * 10 + TERM_RANK[m[1]] : 0;
  }
  var PROF = null;
  function buildProfIndex() {
    var idx = {};
    DATA.programs.forEach(function (p) {
      var seen = {};
      p.versions.forEach(function (v) {
        v.groups.forEach(function (g) {
          g.courses.forEach(function (c) {
            if (seen[c.code]) return;
            seen[c.code] = true;
            var h = c.instructors && c.instructors.history;
            if (!h) return;
            h.forEach(function (r) {
              r.names.forEach(function (n) {
                var k = p.id + "|" + n;
                var e = idx[k] || (idx[k] = { name: n, prog: p, courses: {} });
                var ce = e.courses[c.code] || (e.courses[c.code] = { code: c.code, title: c.title, terms: [] });
                ce.terms.push(r.term);
              });
            });
          });
        });
      });
    });
    return Object.keys(idx).map(function (k) { return idx[k]; });
  }
  function profMatches(q) {
    if (!q) return [];
    if (!PROF) PROF = buildProfIndex();
    var terms = q.toLowerCase().split(/\s+/);
    return PROF.filter(function (e) {
      var n = e.name.toLowerCase();
      return terms.every(function (t) { return n.indexOf(t) !== -1; });
    }).sort(function (a, b) {
      var ca = Object.keys(a.courses).length, cb = Object.keys(b.courses).length;
      return cb - ca;
    }).slice(0, 12);
  }
  function rosterMatches(q) {
    if (!q) return [];
    var terms = q.toLowerCase().split(/\s+/), out = [];
    DATA.programs.forEach(function (p) {
      p.faculty.people.forEach(function (x) {
        var s = x.toLowerCase();
        if (terms.every(function (t) { return s.indexOf(t) !== -1; })) out.push({ prog: p, text: x });
      });
    });
    return out;
  }
  function profPanel() {
    var ps = profMatches(state.q), rs = rosterMatches(state.q);
    if (!ps.length && !rs.length) return null;
    var box = el("section", { class: "prog profpanel" });
    box.appendChild(el("h2", { text: "교수 검색 결과" }));
    box.appendChild(el("p", { class: "src", text: "담당 이력은 공식 기록이 있는 경우만 표시됩니다(현재 IU Course Browser 2004-05~2021). 이름은 기록된 그대로 '성 + 이니셜'이라 이름(first name)으로는 검색되지 않습니다. R 505·586·590·686·699·795처럼 개별지도·인턴십·워크숍 과목은 여러 분반이 개설되어 학기 수가 많게 보일 수 있습니다." }));
    ps.forEach(function (e) {
      var list = Object.keys(e.courses).map(function (k) { return e.courses[k]; })
        .sort(function (a, b) { return b.terms.length - a.terms.length; });
      var d = el("details", { class: "course", style: "--tc:" + COLORS[e.prog.id], open: "open" });
      d.appendChild(el("summary", {}, [
        el("span", { class: "code", text: e.name }),
        el("span", { class: "ctitle", text: e.prog.short + " · " + list.length + "개 과목" }),
        el("span", { class: "ccr", text: list.reduce(function (s, c) { return s + c.terms.length; }, 0) + "개 학기 기록" })
      ]));
      var b = el("div", { class: "body" });
      list.forEach(function (c) {
        var ts = c.terms.slice().sort(function (x, y) { return termKey(x) - termKey(y); });
        b.appendChild(el("p", {}, [
          el("b", { text: c.code + " " }), document.createTextNode(c.title),
          el("br"), el("span", { class: "src", text: ts.length + "학기: " + ts.join(", ") })
        ]));
      });
      d.appendChild(b);
      box.appendChild(d);
    });
    rs.forEach(function (r) {
      box.appendChild(el("p", { class: "na", text: r.prog.short + " 교수진: " + r.text + " — 과목별 담당 이력은 공개 자료로 확인 불가." }));
    });
    return box;
  }

  function tally(history) {
    var m = {};
    history.forEach(function (r) { r.names.forEach(function (n) { m[n] = (m[n] || 0) + 1; }); });
    return Object.keys(m).map(function (k) { return [k, m[k]]; })
      .sort(function (a, b) { return b[1] - a[1]; });
  }

  function instructorBlock(i) {
    var box = el("div");
    if (i.status === "history" && i.history.length) {
      var t = tally(i.history);
      box.appendChild(el("p", { class: "src", text: i.note }));
      box.appendChild(el("div", { class: "tally" }, t.map(function (x) {
        return el("span", { class: "chip", text: x[0] + " · " + x[1] + "학기" });
      })));
      var rows = i.history.map(function (r) {
        return el("tr", {}, [el("td", { text: r.term }), el("td", { text: r.names.join(", ") || "(담당자 표기 없음)" })]);
      });
      var tbl = el("table", { class: "hist" }, [
        el("thead", {}, [el("tr", {}, [el("th", { text: "학기" }), el("th", { text: "담당(표기 그대로)" })])]),
        el("tbody", {}, rows)
      ]);
      box.appendChild(el("details", {}, [
        el("summary", { text: "학기별 전체 보기 (" + i.history.length + "개 학기)" }),
        el("div", { class: "histwrap" }, [tbl])
      ]));
    } else {
      box.appendChild(el("p", { class: "na", text: "공개 자료로 확인 불가 — " + i.note }));
    }
    return box;
  }

  function courseNode(c, color) {
    var d = el("details", { class: "course", style: "--tc:" + color });
    d.appendChild(el("summary", {}, [
      el("span", { class: "code", text: c.code }),
      el("span", { class: "ctitle", text: c.title }),
      el("span", { class: "ccr", text: /\d/.test(String(c.cr)) ? c.cr + "학점" : c.cr })
    ]));
    var b = el("div", { class: "body" });

    b.appendChild(el("h4", { text: "코스 설명" }));
    if (c.descKo) {
      b.appendChild(el("p", { text: c.descKo }));
      b.appendChild(el("p", { class: "en", text: "원문: " + c.descEn }));
      b.appendChild(el("p", { class: "src", text: "출처: " + c.descSrc }));
    } else {
      b.appendChild(el("p", { class: "na", text: "공개 자료로 확인 불가 — 공식 카탈로그에서 과목 설명문을 찾지 못함." }));
    }
    if (c.prereq) b.appendChild(el("p", { class: "src", text: "선수/자격 조건(카탈로그): " + c.prereq }));
    if (c.note) b.appendChild(el("p", { class: "src", text: "참고: " + c.note }));

    b.appendChild(el("h4", { text: "실라버스" }));
    if (c.syllabi && c.syllabi.length) {
      c.syllabi.forEach(function (s) { b.appendChild(s.local ? el("a", { href: s.url, target: "_blank", class: "btn", text: s.label }) : link(s.label, s.url, "btn")); });
    } else if (c.courseUrl) {
      b.appendChild(link("공식 과목 페이지", c.courseUrl, "btn"));
    }
    b.appendChild(el("p", { class: c.syllabi && c.syllabi.length ? "src" : "na", text: c.syllabusNote }));

    b.appendChild(el("h4", { text: "담당 교수" }));
    b.appendChild(instructorBlock(c.instructors));

    d.appendChild(b);
    return d;
  }

  function groupNode(g, color) {
    var courses = g.courses.filter(matches);
    if (state.q && !courses.length) return null;
    var wrap = el("section", { class: "group" });
    var h = el("h3", { text: g.title });
    if (g.credits) h.appendChild(el("span", { class: "cr", text: g.credits + "학점" }));
    wrap.appendChild(h);
    if (g.note) wrap.appendChild(el("p", { class: "gnote", text: g.note }));
    courses.forEach(function (c) { wrap.appendChild(courseNode(c, color)); });
    return wrap;
  }

  function render() {
    var p = prog(), v = version(p), color = COLORS[p.id];
    document.getElementById("asof").textContent = DATA.asOf;
    document.documentElement.style.setProperty("--tc", color);

    var tabs = document.getElementById("tabs");
    tabs.textContent = "";
    DATA.programs.forEach(function (x) {
      var b = el("button", { class: "tab", role: "tab", "aria-selected": String(x.id === p.id), style: "--tc:" + COLORS[x.id], text: x.short });
      b.addEventListener("click", function () {
        state.prog = x.id; location.hash = x.id;
        try { localStorage.setItem("cfp.prog", x.id); } catch (e) { /* ignore */ }
        render();
      });
      tabs.appendChild(b);
    });

    var vers = document.getElementById("vers");
    vers.textContent = "";
    if (p.versions.length > 1) {
      p.versions.forEach(function (x) {
        var b = el("button", { class: "ver", role: "tab", "aria-selected": String(x.id === v.id), text: x.label });
        b.addEventListener("click", function () { state.ver[p.id] = x.id; render(); });
        vers.appendChild(b);
      });
    } else {
      vers.appendChild(el("span", { class: "chip", text: v.label }));
    }

    var view = document.getElementById("view");
    view.textContent = "";
    var pp = profPanel();
    if (pp) view.appendChild(pp);
    var card = el("article", { class: "prog" });
    card.appendChild(el("h2", { text: p.univ + " — " + p.program }));
    card.appendChild(el("p", { class: "sub", text: p.unit }));
    card.appendChild(el("p", { class: "status", text: p.yearStatus }));
    card.appendChild(el("p", { class: "src", text: "이 버전의 근거: " + v.source }));
    card.appendChild(el("ul", { class: "summary" }, v.summary.map(function (s) { return el("li", { text: s }); })));

    var any = false;
    v.groups.forEach(function (g) {
      var n = groupNode(g, color);
      if (n) { card.appendChild(n); any = true; }
    });
    if (!any) card.appendChild(el("p", { class: "empty", text: "검색 결과가 없습니다." }));

    card.appendChild(el("h3", { class: "section-title", text: "교수진" }));
    card.appendChild(el("p", { class: "src", text: p.faculty.note }));
    if (p.faculty.people.length) {
      card.appendChild(el("ul", { class: "people" }, p.faculty.people.map(function (x) { return el("li", { text: x }); })));
    }
    card.appendChild(link("공식 교수진 페이지 ↗", p.faculty.url));

    if (p.pdfs.length) {
      card.appendChild(el("h3", { class: "section-title", text: "공식 PDF 바로 보기" }));
      p.pdfs.forEach(function (x) { card.appendChild(link(x[0] + " ↗", x[1], "btn")); });
    }

    card.appendChild(el("h3", { class: "section-title", text: "출처" }));
    card.appendChild(el("ul", { class: "srcs" }, p.sources.map(function (s) {
      return el("li", {}, [link(s[0], s[1])]);
    })));

    view.appendChild(card);
  }

  try {
    var qp = new URLSearchParams(location.search).get("q");
    if (qp) { state.q = qp.trim(); document.getElementById("q").value = state.q; }
  } catch (e) { /* ignore */ }
  document.getElementById("q").addEventListener("input", function (e) { state.q = e.target.value.trim(); render(); });
  window.addEventListener("hashchange", function () {
    var h = location.hash.slice(1);
    if (DATA.programs.some(function (x) { return x.id === h; })) { state.prog = h; render(); }
  });
  render();
})();
