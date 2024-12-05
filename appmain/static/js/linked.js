document.addEventListener('DOMContentLoaded', function() {
  const buttons = document.querySelectorAll('.select-button');
  buttons.forEach(button => {
    button.addEventListener('click', function() {
      const targetUrl = this.getAttribute('data-target');
      if (targetUrl) {
        window.location.href = targetUrl;
      }
    });
  });
});