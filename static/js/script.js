
function myFunction(inputtxt) 
		{

    		var letters = /^[A-Za-z]+$/;  
			if(inputtxt.value.match(letters))  
		    	{  
		      		// the submit button is enabled when a letter key is pressed
		      		$('input[type="submit"]').prop('disabled', false);

		      		return true;  
		    	}	  
			else  
		    	{  
		    		// the submit button is enabled when a non-letter key is pressed
		      		$('input[type="submit"]').prop('disabled', true);
		      		alert("Please enter only letters.");  

		      		return false;  
		    	}  
		
		}



    