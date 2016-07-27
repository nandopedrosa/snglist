/*
 * Custom javascript for Angular functions
 *
 * @author: Fernando Pedrosa
 * @email: fpedrosa@gmail.com
 */

(function () {
    var app = angular.module('songlist', ['smart-table', 'ui.mask', 'ngSanitize', 'rt.select2']);

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
                window.scrollTo(0,0);
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
                window.scrollTo(0,0);
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
                window.scrollTo(0,0);
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
                window.scrollTo(0,0);
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

//-------------------------------- Song Form Controller ------------------------------------------
    app.controller('SongFormController', ['$http', function ($http) {
        var songCtlr = this;             
        songCtlr.formData = {}; //Form to be serialized        
        songCtlr.message = ''; //Error or Success message

        //Fetch Form Data from the backend (sent by WTForms)        
        songCtlr.formData.songid = $('#songid').attr('value');
        songCtlr.formData.title = $('#title').attr('value');
        songCtlr.formData.artist = $('#artist').attr('value');
        songCtlr.formData.key = $('#key').attr('value');
        songCtlr.formData.tempo = $('#tempo').attr('value');
        songCtlr.formData.duration = $('#duration').attr('value');
        songCtlr.formData.notes = $('#notes').text();
        songCtlr.formData.lyrics = $('#lyrics').attr('value');
        

        //Add or Update song
        this.editSong = function () {            
            songCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/edit-song',
                data: $.param(songCtlr.formData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    songCtlr.errors.error = true;                        
                  
                    if(response.data.title != undefined) {
                        songCtlr.errors.title = response.data.title[0];    
                    }

                    if(response.data.artist != undefined) {
                        songCtlr.errors.artist = response.data.artist[0];    
                    }                                                

                    if(response.data.key != undefined) {
                        songCtlr.errors.key = response.data.key[0];    
                    }

                    if(response.data.tempo != undefined) {
                        songCtlr.errors.tempo = response.data.tempo[0];    
                    }

                    if(response.data.duration != undefined) {
                        songCtlr.errors.duration = response.data.duration[0];    
                    }

                    if(response.data.notes != undefined) {
                        songCtlr.errors.notes = response.data.notes[0];    
                    }

                    if(response.data.lyrics != undefined) {
                        songCtlr.errors.lyrics = response.data.lyrics[0];    
                    }
                    
                } else {
                    songCtlr.errors.error = false;                     
                    if (songCtlr.formData.songid == '') { // New band, clear form
                        songCtlr.formData = {};
                        //hard reset CK Editor
                        songCtlr.formData.lyrics = '';
                    }
                }
                songCtlr.message = response.data.msg;
                window.scrollTo(0,0);

            });
        };

        //Import song lyrics/chords
        songCtlr.songUrl = '';
        songCtlr.importError = '';
        songCtlr.importSuccess = '';

        songCtlr.importSong = function() {            
            var urlToBeImported = {'url':songCtlr.songUrl};
            $http({
                method: 'POST',
                url: '/import-song',
                data: $.param(urlToBeImported)                
            }).then(function(response){
                if(response.data.error) {
                    songCtlr.importError = response.data.error;
                } else {
                    songCtlr.importSuccess = response.data.success;
                    songCtlr.formData.lyrics = response.data.html;
                }                
            });
        };

    }]);    

//-------------------------------- Song Report Controller -------------------------------------------------
    app.controller('SongReportController', ['$http', function ($http) {
        var reportCtlr = this;             
        
        reportCtlr.options = [10,25,50,100]; 
        reportCtlr.lyrics = '';
        reportCtlr.songTitle = '';               
        reportCtlr.message = '';

        reportCtlr.songs = []; // List of songs                
        $http.get('/fetch-songs/').success(function(data){                
            reportCtlr.songs = data;                                    
        });      

        this.deleteSong = function(id) {
            reportCtlr.errors = {}; //Init errors    
            var songToBeDeleted = {'id':id};
            $http({
                method: 'POST',
                url: '/delete-song',
                data: $.param(songToBeDeleted)                
            }).then(function(response){
                reportCtlr.errors.error = false;
                //Remove from list
                for (var i = 0; i < reportCtlr.songs.data.length; i++)
                    if (reportCtlr.songs.data[i].id == id) { 
                        reportCtlr.songs.data.splice(i, 1);
                        break;
                }
                reportCtlr.message = response.data.msg;
                window.scrollTo(0,0);
            });
        };           
        
    }]); 

//-------------------------------- Show Form Controller ------------------------------------------
    app.controller('ShowFormController', ['$http', function ($http) {
        var showCtlr = this;             
        showCtlr.formData = {}; //Form to be serialized        
        showCtlr.message = ''; //Error or Success message

        //Fetch Form Data from the backend (sent by WTForms)        
        showCtlr.formData.showid = $('#showid').attr('value');
        showCtlr.formData.bandid = $('#bandid').attr('value');
        showCtlr.formData.name = $('#name').attr('value');
        showCtlr.formData.start = $('#start').attr('value');
        showCtlr.formData.end = $('#end').attr('value');
        showCtlr.formData.address = $('#address').attr('value');
        showCtlr.formData.pay = $('#pay').attr('value');
        showCtlr.formData.contact = $('#contact').text();
        showCtlr.formData.notes = $('#notes').text();
        

        showCtlr.bands = []; // List of bands                
        showCtlr.selectedband = {}; //Selected band
        $http.get('/fetch-bands/').success(function(data){                
                showCtlr.bands = data;                                    
        }); 

        //Total setlist duration
        showCtlr.totalDuration = '00:00:00';

        //Add or Update show
        this.editShow = function () {
            showCtlr.formData.bandid =  showCtlr.selectedband.id;           
            showCtlr.errors = {}; //Init errors              
            $http({
                method: 'POST',
                url: '/edit-show',
                data: $.param(showCtlr.formData)                
            })
            .then(function(response) {              
                if(response.data.error) {                                                               
                    showCtlr.errors.error = true;                        
                  
                    if(response.data.name != undefined) {
                        showCtlr.errors.name = response.data.name[0];    
                    }

                    if(response.data.start != undefined) {
                        showCtlr.errors.start = response.data.start[0];    
                    }                                                

                    if(response.data.end != undefined) {
                        showCtlr.errors.end = response.data.end[0];    
                    }

                    if(response.data.address != undefined) {
                        showCtlr.errors.address = response.data.address[0];    
                    }

                    if(response.data.contact != undefined) {
                        showCtlr.errors.contact = response.data.contact[0];    
                    }

                    if(response.data.pay != undefined) {
                        showCtlr.errors.pay = response.data.pay[0];    
                    }                    
                    
                } else {
                    showCtlr.errors.error = false;

                    if(!showCtlr.formData.showid)
                        showCtlr.formData.showid = response.data.addedid; //The show just added      
                }
                showCtlr.message = response.data.msg;
                window.scrollTo(0,0);

            });
        };

        //Quick Add
        showCtlr.quickList = []; // List of songs for the quick search                           
        $http.get('/fetch-available-songs/' + showCtlr.formData.showid).success(function(data){                
                showCtlr.quickList = data;                                  
        });             

        //Setlist
        showCtlr.setlist = []; 
        $http.get('/fetch-setlist/' + showCtlr.formData.showid).success(function(data){                
                showCtlr.setlist = data; 
                showCtlr.calculateTotalDuration();                                 
        });             


        showCtlr.songid = '';  
        this.addSong = function() {
            
            if(showCtlr.songid == '' || showCtlr.songid == null)
                return;

            showCtlr.errors = {}; //Init errors    
            var songToBeAdded = {'songid' : showCtlr.songid, 'showid' : showCtlr.formData.showid};
            $http({
                method: 'POST',
                url: '/add-song',
                data: $.param(songToBeAdded)                
            }).then(function(response){
                showCtlr.errors.error = false;

                //Push to setlist
                var songJustAdded = {'id' : response.data.id, 'title' : response.data.title, 
                                    'artist' : response.data.artist, 'duration' : response.data.duration};
                showCtlr.setlist.data.push(songJustAdded);
                showCtlr.calculateTotalDuration();

                //Remove from quick list (don't allow duplicates)
                for (var i = 0; i < showCtlr.quickList.data.length; i++)
                    if (showCtlr.quickList.data[i].id == showCtlr.songid) { 
                        showCtlr.quickList.data.splice(i, 1);
                        break;
                }
                showCtlr.songid = '';
            });
        }; 


        this.removeFromSetlist = function(id) {
            showCtlr.errors = {}; //Init errors    
            var dataRemoveFromSetlist = {'songid' : id, 'showid' : showCtlr.formData.showid};
            $http({
                method: 'POST',
                url: '/remove-from-setlist',
                data: $.param(dataRemoveFromSetlist)                
            }).then(function(response){
                showCtlr.errors.error = false;

                //Back to the Quicklist, sorted Alphabetically
                 var songJustRemoved = {'id' : response.data.id, 'title' : response.data.title, 'duration' : response.data.duration};
                 showCtlr.quickList.data.push(songJustRemoved);                 
                 showCtlr.quickList.data.sort(function(a, b) {
                     var songA = a.title.toUpperCase();
                     var songB = b.title.toUpperCase();
                    return (songA < songB) ? -1 : (songA > songB) ? 1 : 0;
                 });

                //Remove from the setlist
                for (var i = 0; i < showCtlr.setlist.data.length; i++)
                    if (showCtlr.setlist.data[i].id == id) { 
                        showCtlr.setlist.data.splice(i, 1);
                        break;
                }       
                showCtlr.calculateTotalDuration();                        
            });
        };

        this.calculateTotalDuration = function() {
            var minutes = 0;
            var seconds = 0;
            for(var i = 0; i < showCtlr.setlist.data.length; i++) {
                 if(showCtlr.setlist.data[i].duration && showCtlr.setlist.data[i].duration != '') {
                    var tmp =  showCtlr.setlist.data[i].duration.split(":");
                    minutes +=  parseInt(tmp[0]);
                    seconds += parseInt(tmp[1]);                    
                 }
            }

            function secondsToHms(d) {
                d = Number(d);  
                var h = Math.floor(d / 3600);
                var m = Math.floor(d % 3600 / 60);
                var s = Math.floor(d % 3600 % 60);
                return ((h > 0 ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (s < 10 ? "0" : "") + s); 
            }

            showCtlr.totalDuration = secondsToHms(minutes*60 + seconds);   
        };


        this.moveUp = function(songid) {
            showCtlr.errors = {}; //Init errors  
            var songToBeMoved = {'songid' : songid, 'showid' : showCtlr.formData.showid};              
            $http({
                method: 'POST',
                url: '/move-up',
                data: $.param(songToBeMoved)                
            }).then(function(response){
                showCtlr.errors.error = false;
                $http.get('/fetch-setlist/' + showCtlr.formData.showid).success(function(data){                
                    showCtlr.setlist = data;                                  
                });                       
            });
        };


        this.moveDown = function(songid) {
            showCtlr.errors = {}; //Init errors  
            var songToBeMoved = {'songid' : songid, 'showid' : showCtlr.formData.showid};              
            $http({
                method: 'POST',
                url: '/move-down',
                data: $.param(songToBeMoved)                
            }).then(function(response){
                showCtlr.errors.error = false;
                $http.get('/fetch-setlist/' + showCtlr.formData.showid).success(function(data){                
                    showCtlr.setlist = data;                                  
                });                       
            });
        };



    }]);  

//-------------------------------- Song Report Controller -------------------------------------------------
    app.controller('ShowReportController', ['$http', function ($http) {
        var reportCtlr = this;             
        
        reportCtlr.options = [10,25,50,100];         
        reportCtlr.message = '';

        reportCtlr.shows = []; // List of songs                
        $http.get('/fetch-shows/').success(function(data){                
            reportCtlr.shows = data;                                    
        });      

        this.deleteShow = function(id) {
            reportCtlr.errors = {}; //Init errors    
            var showToBeDeleted = {'id':id};
            $http({
                method: 'POST',
                url: '/delete-show',
                data: $.param(showToBeDeleted)                
            }).then(function(response){
                reportCtlr.errors.error = false;
                //Remove from list
                for (var i = 0; i < reportCtlr.songs.data.length; i++)
                    if (reportCtlr.shows.data[i].id == id) { 
                        reportCtlr.shows.data.splice(i, 1);
                        break;
                }
                reportCtlr.message = response.data.msg;
                window.scrollTo(0,0);
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

//-------------------------------- CK Editor Directive ------------------------------------------
  app.directive('ckEditor', function () {
      return {
        require: '?ngModel',
        link: function (scope, elm, attr, ngModel) {
          var ck = CKEDITOR.replace(elm[0]);
          if (!ngModel) return;
          ck.on('instanceReady', function () {
            ck.setData(ngModel.$viewValue);
          });
          function updateModel() {
            scope.$apply(function () {
              ngModel.$setViewValue(ck.getData());
            });
          }
          ck.on('change', updateModel);
          ck.on('key', updateModel);
          ck.on('dataReady', updateModel);

          ngModel.$render = function (value) {
            ck.setData(ngModel.$viewValue);
          };
        }
      };
    });



})(); //End app