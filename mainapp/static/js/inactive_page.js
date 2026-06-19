(function() {
  let timeout;

  function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      window.location.href = '/';
    }, 2 * 60 * 1000);
  }

  window.addEventListener("load", resetTimer);
  document.addEventListener("keydown", resetTimer);
  document.addEventListener("touchstart", resetTimer, { passive: true });
  document.addEventListener("scroll", resetTimer, { passive: true });
  document.addEventListener("click", resetTimer);
})();