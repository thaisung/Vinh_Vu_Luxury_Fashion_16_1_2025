$(function () {
    if ($('.endDateTime').length) {
        // Grab the current date
        // var currentDate = new Date($('.endDateTime').val());
        var currentDate = Date.parse(parseDateString($('.endDateTime').val()));

        // Set some date in the past. In this case, it's always been since Jan 1
        // var pastDate  =  new Date();
        var pastDate = new Date().getTime();
        // Calculate the difference in seconds between the future and current date
        var diff = currentDate / 1000 - pastDate / 1000;

        clock = $('.clock').FlipClock(diff, {
            clockFace: 'DailyCounter',
            autoStart: false,
            language: 'vietnamese'
        });

        clock.setTime(diff);
        clock.setCountdown(true);
        clock.start();
    }

    function parseDateString (dateString) {
        var matchers = [];
        matchers.push(/^[0-9]*$/.source);
        matchers.push(/([0-9]{1,2}\/){2}[0-9]{4}( [0-9]{1,2}(:[0-9]{2}){2})?/.source);
        matchers.push(/[0-9]{4}([\/\-][0-9]{1,2}){2}( [0-9]{1,2}(:[0-9]{2}){2})?/.source);
        matchers = new RegExp(matchers.join("|"));
        if (dateString instanceof Date) {
            return dateString;
        }
        if (String(dateString).match(matchers)) {
            if (String(dateString).match(/^[0-9]*$/)) {
                dateString = Number(dateString);
            }
            if (String(dateString).match(/\-/)) {
                dateString = String(dateString).replace(/\-/g, "/");
            }
            return new Date(dateString);
        } else {
            throw new Error("Couldn't cast `" + dateString + "` to a date object.");
        }
    }
})