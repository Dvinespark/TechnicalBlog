$(document).ready(function(){
    $('#deleteBlogModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let recipient = button.data('blogid'); // Extract info from data-* attributes
        console.log(recipient);
        let data = {
            'blog_id': recipient
        };
        $('#cancel_button').on('click', function (e) {
            $('#deleteBlogModal').modal('toggle');
            return false;
        });
        $('#deleteblog_button').on('click', function (e){
            console.log("delete button clicked");
            $.ajax({
                type: 'post',
                url: "blogs/delete",
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


    $('#addBlogModal').on('show.bs.modal', function (event) {
        $('#cancel_button').on('click', function (e) {
            $('#addBlogModal').modal('toggle');
            return false;
        });
        $('#addblog_button').on('click', function (e){
            // Create blog
            let params = {};
            $.each($('#add_blog').serializeArray(), function (index, value) {
                params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
            });
            let form_data = new FormData();
            for(let key in params){
                form_data.append(key, params[key]);
            }
            form_data.append('photo_url', $("#blog-image")[0].files[0]);
            // form_data.append('file', $('#blog-image').prop('files')[0]);
            // form_data.append('data', params);
            // console.log(form_data);
            // var form_data1 = new FormData();
            // form_data1.append('file', $('#blog-image').prop('files')[0]);

            $.ajax({
                type: 'post',
                url: "blogs/create",
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
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
    $('#editBlogModal').on('show.bs.modal', function (event) {

        $('#blogEditActive').click(function() {
                $('#blogEditActive').val($(this).is(':checked'));
        });

        $('#cancel_button').on('click', function (e) {
            $('#editBlogModal').modal('toggle');
            return false;
        });

        // populate values
        let row = $(event.relatedTarget).closest("tr")       // Finds the closest row <tr>
        let tds = row.find("td");             // Finds all children <td> elements
        console.log(tds);

        // $.each($tds, function() {               // Visits every single <td> element
        //     console.log($(this).text());        // Prints out the text within the <td>
        // });

        $("#edit_blog input[name=title]").val($(tds[0]).text());
        $("#edit_blog input[name=short_description]").val($(tds[1]).text());
        $("#edit_blog textarea[name=long_description]").val($(tds[2]).text());
        $("#edit_blog select[name=blog_type]").val($(tds[4]).text());
        $("#edit_blog select[name=blog_tech]").val($(tds[5]).text());
        $("#blogEditActive").prop("checked", $(tds[6]).text() === "true");

        $("#blogEditActive").val($(tds[6]).text() === "true");

        // edit blogblogEditActive
        $('#editblog_button').on('click', function (e){
            let button = $(event.relatedTarget); // Button that triggered the modal
            let recipient = button.data('blogid'); // Extract info from data-* attributes
            let params = {};
            $.each($('#edit_blog').serializeArray(), function (index, value) {
                params[value.name] = params[value.name] ? params[value.name] || value.value : value.value;
            });
            params['blog_id'] = recipient;


            let form_data = new FormData();
            for(let key in params){
                form_data.append(key, params[key]);
            }
            if ($("#blog-uimage")[0].files.length > 0) {
                form_data.append('photo_url', $("#blog-uimage")[0].files[0]);
            }
            $.ajax({
                type: 'post',
                url: "blogs/edit",
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
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
