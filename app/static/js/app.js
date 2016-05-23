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

    	var ctrl = this;
    	ctrl.errors = {}; //List of errors   	     	
    	ctrl.formData = {}; //Form to be serialized
    	ctrl.message = ''; //Error or Success message


        //Sends a new contact message and handles the response
        this.sendMessage = function () {
            $http.post('/send-message', ctrl.formData)
            	.then(function(response) {
                	console.log(response.data);
                	if(response.data.error) {                		
                		ctrl.errors.error = true;                		
                		ctrl.errors.name = response.data.name[0];
                		ctrl.errors.email = response.data.email[0];
                		ctrl.errors.message = response.data.message[0];                		
                	} else {
                		ctrl.errors.error = false;                		
                	}
                	ctrl.message = response.data.msg;
            	});
        };
    }]);

})();