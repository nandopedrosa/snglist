/*
 * Custom javascript for Angular functions
 *
 * @author: Fernando Pedrosa
 * @email: fpedrosa@gmail.com
 */

(function () {
    var app = angular.module('songlist', []);

    app.config(['$interpolateProvider', '$httpProvider', function ($interpolateProvider, $httpProvider) {
        //Change template start and end symbol to play nice with Flask's Jinja2 Templates
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');

        //Setup default AJAX post request headers
        $httpProvider.defaults.headers.post = {'Content-Type': 'application/x-www-form-urlencoded', 
                                                'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')};        
    }]);    

    //-------------------------------- NavBar Controller ------------------------------------------
    app.controller('NavBarController', ['$http', function ($http) {

        //Changes the application language - from English to Portuguese or vice-versa
        this.changeLanguage = function () {
            $http.post('/change-language').then(function(response) {
                window.location.reload();
            });
        };
    }]);
 
    //-------------------------------- Contact Form Controller ------------------------------------------
    app.controller('ContactFormController', ['$http', function ($http) {

    	var contactCtlr = this;    	     	
    	contactCtlr.formData = {}; //Form to be serialized
    	contactCtlr.message = ''; //Error or Success message

        //Sends a new contact message and handles the response
        this.sendMessage = function () {
            contactCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/send-message',
                data: $.param(contactCtlr.formData)                
            })
            .then(function(response) {            	
            	if(response.data.error) {                		                                		
                    contactCtlr.errors.error = true;                		
            		
                    if(response.data.name != undefined) {
                        contactCtlr.errors.name = response.data.name[0];
                    }

                    if(response.data.email != undefined) {
                        contactCtlr.errors.email = response.data.email[0];    
                    }

                    if(response.data.message != undefined) {
                        contactCtlr.errors.message = response.data.message[0];                          
                    }            		
            		
            	} else {
            		contactCtlr.errors.error = false;                		
            	}
            	contactCtlr.message = response.data.msg;
        	});
        };
    }]);

})();