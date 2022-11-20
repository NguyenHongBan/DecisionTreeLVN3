$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				outlook : $('#outlookI :selected').text(),
                        humidity : $('#humidityI :selected').text(),
                        temp : $('#tempI :selected').text(),
                        wind : $('#windI :selected').text()
			},
			type : 'POST',
			url : '/process'
		})
		.done(function(data) {
			if(data.result == "Yes")
				$('#textResult').text('YES. Today the weather is very well, so you can play tennis!!!');
			else
			{
				if(data.result == "No")
					$('#textResult').text('No. Today the weather is bad, so you can not play tennis!!!');
				else
					$('#textResult').text("We haven't result!!!");
			}
		});

		event.preventDefault();
		$('.container-result').css({"display": "flex"})
	});
	$('.container-result').click(function() {
		$('.content-result').css({"animation": "close linear .4s forwards"})
    	setTimeout(function(){
			$('.content-result').css({"animation": "show linear .4s forwards"})
			$('.container-result').css({"display": "none"})
		}, 400);
	})
	$('.content-result').click(function() {
		event.stopPropagation();
	})
});