// mjoar.com v2: Farbwahl auf der Produktseite. Die Kaufen-Links je Farbe stehen im HTML (data-kaufen), erzeugt aus der
// einen Konstante KAUFEN in _build/site.py. Ohne Wahl (und ohne JavaScript) zeigt der Knopf auf die Kanne ohne Farbwahl.
// Ruhige Reveals: nur mit JavaScript (Klasse .js im Kopf gesetzt) und ohne reduzierte Bewegung, sonst sofort sichtbar.
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
    if (!gewaehlt) return;
    if (knopf) knopf.href = gewaehlt.getAttribute('data-kaufen');
    bilder.forEach(function (bild) {
      var an = bild.getAttribute('data-farbe') === farbe;
      bild.classList.toggle('aktiv', an);
      if (an) bild.removeAttribute('loading');
    });
    if (merken && history.replaceState) history.replaceState(null, '', '#' + farbe);
  }

  wahl.forEach(function (eingabe) {
    eingabe.addEventListener('change', function () { setze(eingabe.value, true); });
  });
  // Ohne Wahl bleibt der Knopf auf der Kanne ohne Farbwahl; ein Anker (#juniper …) von der Startseite wählt vor.
  var anker = location.hash.replace('#', '');
  if (anker && document.querySelector('.farbwahl input[value="' + anker + '"]')) setze(anker, false);
})();
