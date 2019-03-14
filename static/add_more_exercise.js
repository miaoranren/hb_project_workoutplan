

    $(function() {    
        $('#exercise-form').on('submit', evt => {
            evt.preventDefault();

            const formData = {
                equipment: $('.equipment_checkboxes').val(),
                category: $('.category_checkboxes').val()
            };
            console.log(formData);
             
            $.get('/choose_exercises.json', formData, (results) => {
                const exercise = results;
                var list_html = "<br>"
                list_html += "Results:"
                list_html += "<ul>";
                for (var i = 0; i < exercise.length; i++) {
                    var obj = exercise[i];
                    list_html += "<a class='list-group-item list-group-item-action' data-id=" + obj.exercise_id + ">" + obj.name ;
                }
                list_html += "</ul>"
                $('#exercise_result').html(list_html);
            });
        });
    });

    $(function() {
        $('#exercise_result').on('click', function(evt) {
            evt.preventDefault();

            const $evt = $(evt.target);
            const id = $evt.data('id');
            const url = '/addexercises/' + id;
            console.log("id: ", id);

            $.get('/search/' + id, id);
            // $('.detail-form').attr('action', url);
            $('.detail-form').toggle();
        });
    });

    $(function() {
        $('.detail-form').on('submit', function(evt) {
            evt.preventDefault();


            const formData = {
                numberofsets: $('#set').val(),
                reps: $('#rep').val(),
                repunit: $('#repunit').val(),
                weights: $('#weights').val(),
                weightunit: $('#weightunit').val()
            };
            console.log(formData);
            $.post('/addexercises', formData)
            $(".success-info").css("display","block");
            $(".success-info").delay(3000).fadeOut();

        });
    });

    $(function(){
        $('.done').on('click',function(){
            location.href = '/addexercises'
        });
    });
