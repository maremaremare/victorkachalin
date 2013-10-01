/**
 * This file contains the functionality for initializing all the scripts in the
 * site and also there are some main initial settings included here, such as
 * setting rounded corners automatically, setting the Twitter functionality,
 * etc.
 * 
 * @author Pexeto
 */

var pexetoSite = {
	initSite : function() {
		
		// set the contact form functionality
		pexetoContactForm.set();
		
		$("ul.sf-menu").superfish();
		
		//set the tabs functionality
		$("ul.tabs").tabs("div.panes > div");
		
		//set the accordion functionality
		$("#accordion").tabs("#accordion div.pane", {tabs: 'h2', effect: 'slide', initialIndex: 0});

		
	},
	
	
	initializeMap:function(long, lat) {
    var latlng = new google.maps.LatLng(long, lat);
    var myOptions = {
      zoom: 8,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map-canvas"),
        myOptions);
  },

	
	/**
	 * Loads the Nivo image slider.
	 */
	loadNivoSlider : function(obj, effect, showButtons, showArrows) {
		// load the Nivo slider
		$(window)
				.load(function() {
					obj.nivoSlider( {
						effect : effect, // Specify sets like:
						// 'fold,fade,sliceDown'
						slices : 15,
						animSpeed : 800,
						pauseTime : 3000,
						startSlide : 0, // Set starting Slide (0 index)
						directionNav : showArrows, // Next & Prev
						directionNavHide : true, // Only show on hover
						controlNav : showButtons, // 1,2,3...
						controlNavThumbs : false, // Use thumbnails for
						// Control
						// Nav
						controlNavThumbsFromRel : false, // Use image rel for
						// thumbs
						keyboardNav : true, // Use left & right arrows
						pauseOnHover : true, // Stop animation while hovering
						manualAdvance : false, // Force manual transitions
						captionOpacity : 0.8, // Universal caption opacity
						beforeChange : function() {
						},
						afterChange : function() {
						},
						slideshowEnd : function() {
						} // Triggers after all slides have been shown
					});

					// remove numbers from navigation
						$('.nivo-controlNav a').html('');
						$('.nivo-directionNav a').html('');

						// center the slider navigation
						var slideNumber = $('.nivo-controlNav a').length;
						var slideLeft = 960 / 2 - slideNumber * 21 / 2;
						$('.nivo-controlNav:first').css( {
							left : slideLeft
						});
		    });
	}

};

/**
 * Contains the functionality of the send email form. Makes the validation and
 * sends the message.
 */
pexetoContactForm = {
	emptyNameMessage : 'Please fill in your name',
	invalidEmailMessage : 'Please insert a valid email address',
	emptyQuestionMessage : 'Please write your question',
	sentMessage : 'Message Sent',
	set : function() {
		 $("#address_div").hide()
		this.setSendButtonClickHandler();
		this.setInputClickHandler();
		this.setRadioButtonClickHandler();
	},

	/**
	 * Sets the send button click event handler. Validates the inputs and if they are
	 * not valid, displays error messages. If they are valid- makes an AJAX request to the
	 * PHP script to send the message.
	 */
	setRadioButtonClickHandler : function() {
	// var checked = $("input[#id_delivery_1]:checked").val();
	//  if (checked) {
 //        $("#address_div").toggle();
$('input:radio').click(function(){
	$("#address_div").toggle();
    if ($("#id_delivery_1").is(':checked')) { $("#address_div").show();} 
 if ($("#id_delivery_2").is(':checked')) {$("#address_div").hide();}

  });
		
	}, 


    	

	setSendButtonClickHandler : function() {
		$("#send_button")
				.click(function(event) {

					event.preventDefault();
					// valid = true;

					// 	// remove previous validation error messages and warning styles
					// 	$("#name_text_box").removeClass('invalid');
					// 	$("#email_text_box").removeClass('invalid');
					// 	$("#question_text_area").removeClass('invalid');
					// 	$('#invalid_input').hide();
					// 	$('#sent_successful').hide();
					// 	$('.question_icon').remove();
					// 	$('.contact_message').remove();

					// 	// verify whether the name text box is empty
					// 	var nameTextBox = $("#name_text_box");
					// 	var name = nameTextBox.val();
					// 	if (name == '' || name == null) {
					// 		nameTextBox.addClass('invalid');
					// 		valid = false;
					// 		$(
					// 				'<div class="question_icon"></div><div class="contact_message"><p>' + pexetoContactForm.emptyNameMessage + '</p></div>')
					// 				.insertAfter(nameTextBox);
					// 	}

					// 	// verify whether the inserted email address is valid
					// 	var emailTextBox = $("#email_text_box");
					// 	var email = emailTextBox.val();
					// 	if (!pexetoContactForm.isValidEmailAddress(email)) {
					// 		emailTextBox.addClass('invalid');
					// 		valid = false;
					// 		$(
					// 				'<div class="question_icon"></div><div class="contact_message"><p>' + pexetoContactForm.invalidEmailMessage + '</p></div>')
					// 				.insertAfter(emailTextBox);
					// 	}

					// 	// verify whether the question text area is empty
					// 	var phoneTextBox = $("#phone_text_box");
					// 	var phone = phoneTextBox.val();
					// 	if (phone == '' || phone == null) {
					// 		phoneTextBox.addClass('invalid');
					// 		valid = false;
					// 		$(
					// 				'<div class="question_icon"></div><div class="contact_message"><p>' + pexetoContactForm.emptyQuestionMessage + '</p></div>')
					// 				.insertAfter(phoneTextBox);
					// 	}

					// 	if (!valid) {
					// 		//the form inputs are not valid
					// 		$('.contact_message').animate( {
					// 			opacity : 0
					// 		}, 0).hide();
					// 		$('.question_icon').hover(
					// 				function() {
					// 					$(this).css( {
					// 						cursor : 'pointer'
					// 					});
					// 					$(this).siblings('.contact_message')
					// 							.stop().show().animate( {
					// 								opacity : 1
					// 							}, 200);
					// 				},
					// 				function() {
					// 					$(this).siblings('.contact_message')
					// 							.stop().animate( {
					// 								opacity : 0
					// 							}).hide();
					// 				});

					// 		$('#invalid_input').show();
					// 	} else {
					// 		//the form inputs are valid
							
					// 		// show the loading icon
					// 		$('#contact_status').html(
					// 				'<div class="contact_loader"></div>');

					// 		// the data is valid, sumbit the form
							$('#submit_form').submit();

						// }
					});
	},

	setInputClickHandler : function() {
		$('.form_input').click(function() {
			$(this).removeClass('invalid');
		});

		$('.form_input').live('keydown', function(e) {
			var keyCode = e.keyCode || e.which;

			if (keyCode == 9) {
				var index = $('.form_input').index($(this));
				$('.form_input').eq(index + 1).removeClass('invalid');
			}
		});
	},

	/**
	 * Checks if an email address is a valid one.
	 * 
	 * @param emailAddress
	 *            the email address to validate
	 * @return true if the address is a valid one
	 */
	isValidEmailAddress : function(emailAddress) {
		var pattern = new RegExp(
				/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
		return pattern.test(emailAddress);
	}
};
