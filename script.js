document.getElementById('year').textContent = new Date().getFullYear();

document.querySelectorAll('.reveal').forEach(el => {
  let delay = 0;
  if (el.classList.contains('d1')) delay = 120;
  if (el.classList.contains('d2')) delay = 240;
  if (el.classList.contains('d3')) delay = 360;
  el.animate([
    { opacity: 0, transform: 'translateY(10px)' },
    { opacity: 1, transform: 'translateY(0)' }
  ], {
    duration: 1100,
    delay,
    fill: 'forwards',
    easing: 'cubic-bezier(.22,1,.36,1)'
  });
});
