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
    var hay = [c.code, c.title, c.descEn, c.descKo, c.note].join(" ").toLowerCase();
    return state.q.toLowerCase().split(/\s+/).every(function (t) { return hay.indexOf(t) !== -1; });
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

  document.getElementById("q").addEventListener("input", function (e) { state.q = e.target.value.trim(); render(); });
  window.addEventListener("hashchange", function () {
    var h = location.hash.slice(1);
    if (DATA.programs.some(function (x) { return x.id === h; })) { state.prog = h; render(); }
  });
  render();
})();
