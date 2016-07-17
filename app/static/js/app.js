/*
 * Custom javascript for Angular functions
 *
 * @author: Fernando Pedrosa
 * @email: fpedrosa@gmail.com
 */

(function () {
    var app = angular.module('songlist', ['smart-table']);

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

        var navCtlr = this;
        navCtlr.language = {};
        navCtlr.language.code = $('#about').text() == 'Sobre' ? 'pt' : 'en';
        
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
                        window.location = baseURL;                        
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

                    if(response.data.currentpassword != undefined) {
                        profileCtlr.errors.currentpassword = response.data.currentpassword[0];
                    }               
                    
                } else {
                    profileCtlr.errors.error = false;                       
                }
                profileCtlr.message = response.data.msg;
            });
        };

        this.deleteUser = function () {
            profileCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/delete-user'                
            })
            .then(function successCallback(response) {
                profileCtlr.errors.error = false;   
                baseURL = window.location.protocol + "//" + window.location.host;
                window.location.href = baseURL;     
            }, function errorCallback(response) {
                profileCtlr.errors.error = true;   
                profileCtlr.message = 'There as an error processing your request. Please contact the site administrator';
            });
        };    
    }]);

//-------------------------------- Band Form Controller ------------------------------------------
    app.controller('BandFormController', ['$http', function ($http) {
        var bandCtlr = this;             
        bandCtlr.formData = {}; //Form to be serialized        
        bandCtlr.message = ''; //Error or Success message

        //Fetch Form Data from the backend (sent by WTForms)        
        bandCtlr.formData.name = $('#name').attr('value');
        bandCtlr.formData.style = $('#style').attr('value');
        bandCtlr.formData.bandid = $('#bandid').attr('value');

        //Add or Update band
        this.editBand = function () {            
            bandCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/edit-band',
                data: $.param(bandCtlr.formData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    bandCtlr.errors.error = true;                        
                  
                    if(response.data.name != undefined) {
                        bandCtlr.errors.name = response.data.name[0];    
                    }

                    if(response.data.style != undefined) {
                        bandCtlr.errors.style = response.data.style[0];    
                    }                                                
                    
                } else {
                    bandCtlr.errors.error = false;                     
                    if (bandCtlr.formData.bandid == '') // New band, clear form
                        bandCtlr.formData = {};
                }
                bandCtlr.message = response.data.msg;
            });
        };

        bandCtlr.memberData = {}; // Band members form    
        bandCtlr.memberData.bandid = $('#bandid').attr('value');   
        bandCtlr.members = []; //Members list

        if (typeof bandCtlr.memberData.bandid != "undefined" && bandCtlr.memberData.bandid != '') {
            $http.get('/fetch-members/' + bandCtlr.memberData.bandid).success(function(data){                
                bandCtlr.members = data;
            });  
        }

        //Add or Update a band member
        this.addMember = function () {   
            bandCtlr.memberData.bandid = $('#bandid').attr('value');   
            bandCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/add-member',
                data: $.param(bandCtlr.memberData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    bandCtlr.errors.error = true;                        
                  
                    if(response.data.member_name != undefined) {
                        bandCtlr.errors.member_name = response.data.member_name[0];    
                    }

                    if(response.data.member_email != undefined) {
                        bandCtlr.errors.member_email = response.data.member_email[0];    
                    }                                                
                    
                } else {
                    //Member added
                    bandCtlr.errors.error = false;                         
                    bandCtlr.members.data.push({name : bandCtlr.memberData.member_name, 
                        email : bandCtlr.memberData.member_email });
                    bandCtlr.memberData = {}; // Band members form                    
                }
                bandCtlr.message = response.data.msg;
            });
        }; 

        this.deleteMember = function(id) {
            bandCtlr.errors = {}; //Init errors    
            var memberToBeDeleted = {'id':id};
            $http({
                method: 'POST',
                url: '/delete-member',
                data: $.param(memberToBeDeleted)                
            }).then(function(response){
                bandCtlr.errors.error = false;
                //Remove from list
                for (var i = 0; i < bandCtlr.members.data.length; i++)
                    if (bandCtlr.members.data[i].id == id) { 
                        bandCtlr.members.data.splice(i, 1);
                        break;
                }
            });
        };    

    }]);    

//-------------------------------- Band Report Controller -------------------------------------------------
app.controller('BandReportController', ['$http', function ($http) {
        var reportCtlr = this;             
        
        reportCtlr.options = [10,25,50,100];                
        reportCtlr.message = '';

        reportCtlr.bands = []; // List of bands                
        $http.get('/fetch-bands/').success(function(data){                
            reportCtlr.bands = data;                                    
        });      

        this.deleteBand = function(id) {
            reportCtlr.errors = {}; //Init errors    
            var bandToBeDeleted = {'id':id};
            $http({
                method: 'POST',
                url: '/delete-band',
                data: $.param(bandToBeDeleted)                
            }).then(function(response){
                reportCtlr.errors.error = false;
                //Remove from list
                for (var i = 0; i < reportCtlr.bands.data.length; i++)
                    if (reportCtlr.bands.data[i].id == id) { 
                        reportCtlr.bands.data.splice(i, 1);
                        break;
                }
                reportCtlr.message = response.data.msg;
            });
        };           
        
    }]);    

//-------------------------------- Confirmation Dialog Directive ------------------------------------------
    app.directive('confirmationNeeded', function () {
        return {
            priority: 1,
            terminal: true,
            link: function (scope, element, attr) {
              var msg = attr.confirmationNeeded || $('meta[name="confirmation"]').attr('content');
              var clickAction = attr.ngClick;
              element.bind('click',function () {
                if ( window.confirm(msg) ) {
                  scope.$eval(clickAction)
                }
              });
            }
        };
    });     

})(); //End app