
    $(document).ready(function() {
        let events = [];
        {% for workout in workout_schedule %}
        event = {};
        event.id = '{{ workout.workout_id }}'
        event.title = '{{ workout.description }}'
        event.start = '{{ workout.scheduled_at }}'

        event.description = ''
        {% for exercise in workout.exercises %}
            event.description += '<li class="exercise-calendar">{{ exercise.name }}</li>'
        {% endfor %}
        console.log(event.description)

        events.push(event)
        {% endfor %}
        console.log(events)
        $('#calendar').fullCalendar({
            header: {
                close: 'fa-times',
                prev: 'fa-chevron-left',
                next: 'fa-chevron-right',
                
            },
            height: 650,
            aspectRatio: 1,
            events: events,
            editable: true,
            themeSystem:'bootstrap4',
            eventDrop: function(event, dayDelta, revertFunc) {
                let msg = "Are you sure you want to move the workout \"" +
                        event.title +
                        "\" to " +
                        event.start.format() +
                        "?"
                if (!confirm(msg)) {
                    revertFunc();
                }
                else {
                    $.ajax({
                        url: '/reschedule_workout',
                        data: {
                            id: event.id,
                            newDate: event.start.format()
                        },
                        type: 'POST',
                        success: function() {
                            location.reload();
                        }
                    });
                }
            },

            eventRender: function(event, $el) {
                $el.popover({
                    title: event.title,
                    html:true,
                    content: event.description,
                    animation: true,
                    trigger: 'hover',
                    placement: 'top',
                    container: '#calendar'
                });
                
            },

            eventClick: function(event, jsEvent, view) {
                location.href = '/click_day_details/' + event.id
            
            }
            
        });
    });

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
               $('.detail-form').toggle();

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
