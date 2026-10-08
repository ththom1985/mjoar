// mjoar.com v4 (One-Pager). Ohne JavaScript funktioniert alles: Anker springen, der Kaufen-Knopf zeigt auf die Kanne
// ohne Farbwahl, Inhalte sind sofort sichtbar. Mit JavaScript: ruhige Reveals (unverändert), Farbwahl, aktiver Abschnitt
// in der Navigation, Mobilmenü schließt nach dem Sprung, Sprachwechsel behält den Abschnitt, alte Anker führen weiter.
(function () {
  var ziele = document.querySelectorAll('[data-reveal]');
  var ruhig = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (ruhig || !('IntersectionObserver' in window)) {
    ziele.forEach(function (el) { el.classList.add('sichtbar'); });
    return;
  }
  var io = new IntersectionObserver(function (eintraege) {
    eintraege.forEach(function (eintrag) {
      if (eintrag.isIntersecting) { eintrag.target.classList.add('sichtbar'); io.unobserve(eintrag.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  ziele.forEach(function (el) { io.observe(el); });
})();

// Farbwahl: Die Kaufen-Links je Farbe stehen im HTML (data-kaufen), erzeugt aus der Konstante KAUFEN in _build/site.py.
(function () {
  var wahl = document.querySelectorAll('.farbwahl input[name="farbe"]');
  if (!wahl.length) return;
  var knopf = document.getElementById('kaufen');
  var bilder = document.querySelectorAll('.farbbild');

  function setze(farbe, merken) {
    var gewaehlt = null;
    wahl.forEach(function (eingabe) {
      if (eingabe.value === farbe) { eingabe.checked = true; gewaehlt = eingabe; }
    });
    if (!gewaehlt) return false;
    if (knopf) knopf.href = gewaehlt.getAttribute('data-kaufen');
    bilder.forEach(function (bild) {
      var an = bild.getAttribute('data-farbe') === farbe;
      bild.classList.toggle('aktiv', an);
      if (an) bild.removeAttribute('loading');
    });
    if (merken && history.replaceState) history.replaceState(null, '', '#' + farbe);
    return true;
  }

  wahl.forEach(function (eingabe) {
    eingabe.addEventListener('change', function () { setze(eingabe.value, true); });
  });
  // Ein Farbanker (#juniper …, auch von den alten Produktseiten) wählt vor und springt zur Produktansicht.
  var anker = location.hash.replace('#', '');
  if (anker && setze(anker, false)) {
    var lun = document.getElementById('lun');
    if (lun) lun.scrollIntoView();
  }
})();

// Alte Anker der früheren Seiten auf die Abschnitte des One-Pagers.
(function () {
  var de = document.documentElement.lang === 'de';
  var gut = de ? '#gut-zu-wissen' : '#good-to-know', ueber = de ? '#ueber-uns' : '#about';
  var alt = {
    '#colour': '#lun', '#colours': '#lun', '#farben': '#lun', '#object': '#lun', '#craft': '#details',
    '#honest': gut, '#groesse': gut, '#pflege': gut, '#ausgepackt': gut, '#gebrauch': '#latte-art',
    '#story': ueber, '#founders': ueber, '#name': ueber, '#early': ueber, '#partners': ueber, '#wer': ueber, '#hero': '#top'
  };
  var neu = alt[location.hash];
  var ziel = neu && document.getElementById(neu.slice(1));
  if (!ziel) return;
  if (history.replaceState) history.replaceState(null, '', neu);
  ziel.scrollIntoView();
})();

// Navigation: aktiver Abschnitt dezent markiert; Mobilmenü schließt nach dem Sprung; Sprachwechsel behält den Abschnitt.
(function () {
  var menu = document.querySelector('.menu-mobil');
  document.querySelectorAll('.menu-mobil a').forEach(function (a) {
    a.addEventListener('click', function () { if (menu) menu.removeAttribute('open'); });
  });
  var abschnitte = Array.prototype.slice.call(document.querySelectorAll('main > section[id]'));
  if (!abschnitte.length) return;
  var links = document.querySelectorAll('.menu-desktop a, .menu-mobil a');

  function aktuell() {
    var linie = window.innerHeight * 0.35, treffer = null;
    abschnitte.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top <= linie && r.bottom > linie) treffer = el.id;
    });
    return treffer;
  }
  var aktiv;
  function markiere() {
    var neu = aktuell();
    if (neu === aktiv) return;
    aktiv = neu;
    links.forEach(function (a) {
      if (a.getAttribute('href') === '#' + aktiv) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }
  var geplant = false;
  window.addEventListener('scroll', function () {
    if (geplant) return;
    geplant = true;
    window.requestAnimationFrame(function () { geplant = false; markiere(); });
  }, { passive: true });
  markiere();

  // Sprachwechsel: gleicher Abschnitt in der anderen Sprache
  var paare = { 'einstieg': 'intro', 'gut-zu-wissen': 'good-to-know', 'ueber-uns': 'about' };
  var umgekehrt = {};
  Object.keys(paare).forEach(function (k) { umgekehrt[paare[k]] = k; });
  document.querySelectorAll('.sprachen a').forEach(function (a) {
    a.addEventListener('click', function () {
      var hier = document.documentElement.lang, dort = a.getAttribute('hreflang'), id = aktuell();
      if (!id || hier === dort) return;
      var ziel = hier === 'de' ? (paare[id] || id) : (umgekehrt[id] || id);
      a.setAttribute('href', a.getAttribute('href').split('#')[0] + '#' + ziel);
    });
  });
})();
