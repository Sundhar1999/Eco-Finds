$(document).ready(function () {
  $("#forget_password_form").on("submit", function (event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $.post("{% url 'account_recovery' %}", formData, function (data) {
      if (data.success) {
        $("#user_options-forms").addClass("bounceLeft");
        setTimeout(function () {
          $("#forget_password_form_div").hide();
          $("#security_questions_form_div").show();
          $("#user_options-forms").removeClass("bounceLeft");
        }, 1000);
      } else {
        alert(data.error);
      }
    });
  });

  $("#security_questions_form").on("submit", function (event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $.post("{% url 'account_recovery' %}", formData, function (data) {
      if (data.success) {
        $("#user_options-forms").addClass("bounceUp");
        setTimeout(function () {
          $("#security_questions_form_div").hide();
          $("#set_new_password_form_div").show();
          $("#user_options-forms").removeClass("bounceUp");
        }, 1000);
      } else {
        alert(data.error);
      }
    });
  });

  $("#set_new_password_form").on("submit", function (event) {
    event.preventDefault();
    var formData = $(this).serialize();
    $.post("{% url 'account_recovery' %}", formData, function (data) {
      if (data.success) {
        alert("Password has been reset!");
        window.location.href = "{% url 'login' %}";
      } else {
        alert(data.error);
      }
    });
  });
});
