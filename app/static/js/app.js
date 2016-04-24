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

        //Sends a new contact message and handles the response
        this.sendMessage = function () {
            //TODO: post send message
        };
    }]);

})();