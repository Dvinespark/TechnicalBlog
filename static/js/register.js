$(document).ready(function() {
    function validate() {

        var signup_text = $("#signup-text").find("p");

        // validation before calling ajax
        if($("#sign-agree-check").prop("checked") === false){
            signup_text.text("Please check the checkbox to proceed.");
            signup_text.css("color", "red");
            return false
        }
        // check if any field is empty
        let form_data = $("#register-form").serializeArray();
        for(let i in form_data){
            if (!form_data[i].value){
                signup_text.text("Please enter the value for " + form_data[i].name);
                signup_text.css("color", "red");
                return false
            }
        }
        // check if password does not match
        if (form_data[1].value !== form_data[2].value){
            signup_text.text("Entered password does not match");
            signup_text.css("color", "red");
            return false
        }
        return true
    }

    $('#register-form').on('submit',function (e) {
        // calling ajax
        $.ajax({
            type: 'post',
            url: "/register",
            data: $('#register-form').serialize(),
            beforeSend: function (xhr, opts) {
                if (!validate()){
                    xhr.abort();
                    return false;
                }
            },
            success: function (response) {
                console.log(response);
                if(response.status_code){
                    console.log("this part is executing");
                    window.location.href = response.url;
                }
            }
        });
        e.preventDefault();
    });
});
