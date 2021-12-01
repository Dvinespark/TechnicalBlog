
$(document).ready(function(){

    $('#editBlogModal').on('show.bs.modal', function (event) {

        $('#blogEditActive').click(function() {
            $('#blogEditActive').val($(this).is(':checked'));
        });

        $('#e_cancel_button').on('click', function (e) {
            $('#editBlogModal').modal('toggle');
            return false;
        });

        // populate values
        let row = $(event.relatedTarget).closest("tr")       // Finds the closest row <tr>
        let tds = row.find("td");             // Finds all children <td> elements


        $("#edit_blog select[name=blog_type]").val($(tds[4]).text());
        $("#blogEditActive").prop("checked", $(tds[6]).text() === "true");
        $("#blogEditActive").val($(tds[6]).text() === "true");

        // edit blogblogEditActive
        $('#editblog_button').on('click', function (e){
            let button = $(event.relatedTarget); // Button that triggered the modal
            let recipient = button.data('commentid'); // Extract info from data-* attributes
            let params = {};
            $.each($('#edit_blog').serializeArray(), function (index, value) {
                params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
            });
            params['id'] = recipient;


            let form_data = new FormData();
            for(let key in params){
                form_data.append(key, params[key]);
            }
            $.ajax({
                type: 'post',
                url: "comment/edit",
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function (response) {
                    if(response.status_code){
                        window.location.href = response.url;
                    }
                }
            });
            e.preventDefault();
        });
    });

});
