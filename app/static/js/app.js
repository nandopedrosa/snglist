/*
 * Custom javascript for Angular functions
 *
 * @author: Fernando Pedrosa
 * @email: fpedrosa@gmail.com
 */

(function () {
    var app = angular.module('songlist', []);

    //Change template start and end symbol to play nice with Flask's Jinja2 Templates
    app.config(['$interpolateProvider', function ($interpolateProvider) {
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }]);

    //Global Variable used by Form Controllers
    app.value('csrf', $('meta[name="csrf-token"]').attr('content'));

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
    app.controller('ContactFormController', ['$http', 'csrf', function ($http, csrf) {

    	var ctrl = this;    	     	
    	ctrl.formData = {}; //Form to be serialized
    	ctrl.message = ''; //Error or Success message


        //Sends a new contact message and handles the response
        this.sendMessage = function () {
            ctrl.errors = {}; //List of errors              
            $http({
                method: 'POST',
                url: '/send-message',
                data: $.param(ctrl.formData),
                headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': csrf}
            })
            .then(function(response) {            	
            	if(response.data.error) {                		                                		
                    ctrl.errors.error = true;                		
            		
                    if(response.data.name != undefined) {
                        ctrl.errors.name = response.data.name[0];
                    }

                    if(response.data.email != undefined) {
                        ctrl.errors.email = response.data.email[0];    
                    }

                    if(response.data.message != undefined) {
                        ctrl.errors.message = response.data.message[0];                          
                    }            		
            		
            	} else {
            		ctrl.errors.error = false;                		
            	}
            	ctrl.message = response.data.msg;
        	});
        };
    }]);

})();