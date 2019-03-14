$(function() {
        $('.update-exercise').on('submit', function(evt) {
            evt.preventDefault();
            const $this = $(this);
            const exercise_id = $this.find('.to_update').val();
            console.log(exercise_id)
            $.get('/search/' + exercise_id);
            $('#detail-form').attr('data-id', exercise_id);
            $('.detail-form').toggle();
        });
    });
$(function(revertFunc) {
        $('.delete-exericise').on('submit', function(evt) {
            evt.preventDefault();
            const $this = $(this);
            console.log($this);
            const msg = "Are you sure to delete this exercise?";
            // const exercise_id = $this.data('id');
            const exercise_id = $this.find('.to_delete').val();
            console.log("exercise_id:", exercise_id);
            // const exercise_id = $('.to_delete').val();

            if (!confirm(msg)) {
                revertFunc();
            }
            else {
                $.post('/deleteexercises' + '/'+ exercise_id, (results) => {
                    location.reload();
                });
            }
        });
    });
$(function() {
        $('.detail-form').on('submit', function(evt) {
            evt.preventDefault();
            const $this = $(this);
            const exercise_id = $this.find("#detail-form").data('id');
            const formData = {
                numberofsets: $('#set').val(),
                reps: $('#rep').val(),
                repunit: $('#repunit').val(),
                weights: $('#weights').val(),
                weightunit: $('#weightunit').val()
            };
            console.log(formData);
            $.post('/addexercises.json' + '/'+ exercise_id, formData, (results) =>{
               location.reload();

            });
            

        });
    });

$(function(){
        $('.description-button').on('click', function(evt){
                
                const $this = $(this);
        
                const exercise_id = $this.data('exercise_id');
                console.log(exercise_id);
                $.get('/exercises_description.json' + '/' + exercise_id, (results)=>{
                    const exercises_description = results;

                    $('.modal-body').html(exercises_description);
                });
            });
        });

$(function(){
        $('.description-button').on('click', function(evt){
                
                const $this = $(this);
        
                const exercise_id = $this.data('exercise_id');
                console.log(exercise_id);
                $.get('/exercises_name.json' + '/' + exercise_id, (results)=>{
                    const exercises_name = results;

                    $('.modal-title').html(exercises_name);
                });
            });
        });
