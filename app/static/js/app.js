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

        //Setup default AJAX post request headers (gets token from HTML meta header)
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
                url: '/contact',
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
                    contactCtlr.formData = {};          		
            	}
            	contactCtlr.message = response.data.msg;
        	});
        };
    }]);

//-------------------------------- Signup Form Controller ------------------------------------------
    app.controller('SignupFormController', ['$http', function ($http) {

        var signupCtlr = this;             
        signupCtlr.formData = {}; //Form to be serialized
        signupCtlr.message = ''; //Error or Success message

        //Signs up a new user
        this.signup = function () {
            signupCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/signup',
                data: $.param(signupCtlr.formData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    signupCtlr.errors.error = true;                        
                    
                    if(response.data.name != undefined) {
                        signupCtlr.errors.name = response.data.name[0];
                    }

                    if(response.data.email != undefined) {
                        signupCtlr.errors.email = response.data.email[0];    
                    }

                    if(response.data.password != undefined) {
                        signupCtlr.errors.password = response.data.password[0];                          
                    }       

                     if(response.data.password2 != undefined) {
                        signupCtlr.errors.password2 = response.data.password2[0];                          
                    }               
                    
                } else {
                    signupCtlr.errors.error = false;      
                    signupCtlr.formData = {};                  
                }
                signupCtlr.message = response.data.msg;
            });
        };
    }]);
//-------------------------------- Login Form Controller ------------------------------------------
    app.controller('LoginFormController', ['$http', function ($http) {
            var loginCtlr = this;             
            loginCtlr.formData = {}; //Form to be serialized
            loginCtlr.message = ''; //Error or Success message

            //Log in a new user
            this.login = function () {
                loginCtlr.errors = {}; //Init errors              
                $http({
                    method: 'POST',
                    url: '/login',
                    data: $.param(loginCtlr.formData)                
                })
                .then(function(response) {              
                    if(response.data.error) {                                                               
                        loginCtlr.errors.error = true;                        
                      
                        if(response.data.email != undefined) {
                            loginCtlr.errors.email = response.data.email[0];    
                        }

                        if(response.data.password != undefined) {
                            loginCtlr.errors.password = response.data.password[0];                          
                        }                        
                        
                    } else {
                        loginCtlr.errors.error = false;      
                        loginCtlr.formData = {};
                        baseURL = window.location.protocol + "//" + window.location.host;
                        window.location.href = baseURL;
                    }
                    loginCtlr.message = response.data.msg;
                });
            };
        }]);

//-------------------------------- Profile Form Controller ------------------------------------------
    app.controller('ProfileFormController', ['$http', function ($http) {

        var profileCtlr = this;  
        profileCtlr.formData = {}; // Form to be serialized            
        profileCtlr.message = ''; //Error or Success message

        //Fetch Form Data from the backend (sent by WTForms)        
        profileCtlr.formData.name = $('#name').attr('value');

        //Updates the user profile
        this.updateProfile = function () {
            profileCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/profile',
                data: $.param(profileCtlr.formData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    profileCtlr.errors.error = true;                        
                    
                    if(response.data.name != undefined) {
                        profileCtlr.errors.name = response.data.name[0];
                    }

                    if(response.data.password != undefined) {
                        profileCtlr.errors.password = response.data.password[0];                          
                    }       

                     if(response.data.password2 != undefined) {
                        profileCtlr.errors.password2 = response.data.password2[0];                          
                    }               
                    
                } else {
                    profileCtlr.errors.error = false;                       
                }
                profileCtlr.message = response.data.msg;
            });
        };
    }]);

})(); //End app