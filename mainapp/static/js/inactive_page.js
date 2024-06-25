(function() {
  let timeout;

  function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      window.location.href = '/';
    }, 2 * 60 * 1000);
  }

  window.onload = resetTimer;
  document.onmousemove = resetTimer;
  document.onkeypress = resetTimer;
  document.ontouchstart = resetTimer;
  document.onscroll = resetTimer;
  document.onclick = resetTimer;
})();