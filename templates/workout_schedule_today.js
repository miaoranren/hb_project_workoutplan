"use strict";

$(document).ready(function() {
        let events = [];
        {% for workout in workout_schedule %}
        event = {};
        event.id = '{{ workout.workout_id }}'
        event.title = '{{ workout.description }}'
        event.start = '{{ workout.scheduled_at }}'

        event.description = ''
        {% for exercise in workout.exercises %}
            event.description += '<li>{{ exercise.name }}</li>'
        {% endfor %}
        console.log(event.description)

        events.push(event)
        {% endfor %}
        console.log(events)
        $('#calendar').fullCalendar({
            header: {
                left: 'prev,next today',
                center: 'title',
                right: 'month,basicWeek,basicDay'
            },
            height: 650,
            aspectRatio: 1,
            events: events,
            editable: true,

            eventDrop: function(event, dayDelta, revertFunc) {
                let msg = "Are you sure you want to move the workout \"" +
                        event.title +
                        "\" to " +
                        event.start.format() +
                        "?"
                if (!confirm(msg)) {
                    revertFunc();
                }

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
                // alert('clicked');
                // $.ajax({
                //     url: '/click_day_details',
                //     data: {
                //         id: event.id,
                //         date: event.start.format()
                //     },
                //     type:'GET',
                // });
            }
            
        });
    });