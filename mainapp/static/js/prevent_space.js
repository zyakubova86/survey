function validateForm() {
  const textareas = document.querySelectorAll('.responseTextarea');
  const path = window.location.pathname;
  const tooltipTitle = path.includes('/ru/') ? "Не отправляйте пробел!" : "Пробел юборманг!";

  for (let textarea of textareas) {
      const text = textarea.value.trim();

      if (text === '') {
          $(textarea).tooltip({
              title:  tooltipTitle,
              placement: "bottom",
              html: true,
              trigger: "manual",
              template: '<div class="tooltip custom-tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>',
          }).tooltip('show');

          return false;
      } else {
          $(textarea).tooltip('hide');
      }
  }

  return true;
}

$(document).ready(function() {
    // Hide tooltips on focus, input, blur
    $('.responseTextarea').on('focus', function() {
        $(this).tooltip('hide');
    });

    $('.responseTextarea').on('blur', function() {
        $(this).tooltip('hide');
    });

    $('.responseTextarea').on('input', function() {
        $(this).tooltip('hide');
    });

    $('[data-toggle="tooltip"]').tooltip();
});