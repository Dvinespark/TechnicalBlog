$(document).ready(function(){
    $('#deleteBlogModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var recipient = button.data('id'); // Extract info from data-* attributes
        console.log(recipient);
        let data = {
            'username': recipient
        };
        $('#cancel_button').on('click', function (e) {
            $('#deleteBlogModal').modal('toggle');
            return false;
        });
        $('#submit_button').on('click', function (e){
            $.ajax({
                type: 'post',
                url: "users/delete",
                data: data,
                success: function (response) {
                    console.log(response);
                    if(response.status_code){
                        window.location.href = response.url;
                    }
                }
            });
            e.preventDefault();
        });
    });

});
