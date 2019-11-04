// angular.js code goes here
var app = angular.module('ctlgApp', ['ngRoute']);

// configure routes
app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'static/partials/categories.html',
            controller: 'indexController'
        })
        .when('/categ/:id', {
            templateUrl: 'static/partials/category.html',
            controller: 'categoryController',
            resolve: {
                id: function($q, $route) {
                    var deferred = $q.defer(),
                        id = parseInt($route.current.params.id, 10);
                    if (!isNaN(id)) {
                        deferred.resolve(id);
                    } else {
                        deferred.reject('Id is not a number');
                    }
                    return deferred.promise;
                }
            }
        })
        .when('/create-item', {
            templateUrl: 'static/partials/create-item.html',
            controller: 'createItemController'
        })
        .otherwise({
            redirectTo: '/'
        });
});

// controllers
app.controller('indexController', function($scope, $http, $rootScope) {
    $http.get("/?json=all")
        .success(function(data, status, headers) {
            $rootScope.categories = data;
        })
        .error(function(data, status, headers, config) {
            console.log("error retriving all categories")
        });
    // setting current username from the cookie set by server after login
    $rootScope.username = "";
    var name = "username=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            username = c.substring(name.length, c.length);
            // remove quotes from the cookie value
            $rootScope.username = username.replace(/"/g, "");
        }
    }
    $rootScope.alertMsg = function(type, msg) {
        // type must be one of [success, info, danger]
        $('#alertsDiv').removeAttr('hidden');
        $('#alertsDiv').show();

        $('#alertsDiv').removeClass('alert-danger');
        $('#alertsDiv').removeClass('alert-info');
        $('#alertsDiv').removeClass('alert-success');

        $('#alertsDiv').addClass(('alert-' + type));
        $('#alertsDiv').text(msg);

        $('#alertsDiv').delay(4000).hide(0);
    };
});

app.controller('categoryController', function($scope, $http, $rootScope, $routeParams, $location, id) {
    // redirect if this page called directly
    if (typeof $rootScope.categories === 'undefined') {
        $location.path('/');
        return;
    }
    $scope.editItem = function(event) {
        var btnElem = $(event.target).closest('button');
        var data = {};
        data.category = btnElem.attr('data-item-category');
        data.itemName = btnElem.attr('data-mobile-item');
        // passing data as parameter to the controller
        $location.path('/create-item').search(data);
    };
    $scope.deleteItem = function(event) {
        if (confirm('Sure want to delete this item?')) {
            var btnElem = $(event.target).closest('button');
            var data = {};
            data.category = btnElem.attr('data-item-category');
            data.itemName = btnElem.attr('data-mobile-item');

            $http({
                    method: 'DELETE',
                    url: '/item',
                    data: data,
                    headers: {
                        'Content-type': 'application/json;charset=utf-8'
                    }
                })
                .then(function(response) {
                    console.log(response);
                    if (response.data.error) {
                        // show error msg
                        $rootScope.alertMsg('danger', 'Failed to delete item. ' + response.data.error);
                    } else {
                        $rootScope.alertMsg('success', 'Deleted item successfully.');
                        $location.path('/');
                    }
                }, function(rejection) {
                    console.log(rejection.data);
                });
        }
    };
    for (var idx = 0; idx < $rootScope.categories.length; idx++) {
        var element = $rootScope.categories[idx];
        if (element.id == id) {
            $scope.category = element;
            $scope.category.items.forEach(function(item) {
                item.isAuthor = ($rootScope.username == item.username);
            }, this);
            return;
        }
    }

    // no such category id is available redirect to landing page
    $location.path('/');
});

app.controller('createItemController', function($scope, $http, $rootScope, $location, $routeParams) {
    // redirect if this page called directly
    if (typeof $rootScope.categories === 'undefined') {
        $location.path('/');
        return;
    }
    // get the categ titles for loading to the droptdown
    $scope.categoryTitles = [];
    $rootScope.categories.forEach(function(categ) {
        $scope.categoryTitles.push(categ.category)
    }, this);

    $scope.fields = [];
    $scope.action = "Add";

    // get the item if it is called from edit button
    var item;
    var ctgry;

    if ($routeParams.itemName && $routeParams.category) {
        for (var idx = 0; idx < $rootScope.categories.length; idx++) {
            if ($rootScope.categories[idx].category == $routeParams.category) {
                ctgry = $rootScope.categories[idx];
                break;
            }
        }
        for (var iidx = 0; iidx < ctgry.items.length; iidx++) {
            if (ctgry.items[iidx].item == $routeParams.itemName) {
                item = ctgry.items[iidx];
                break;
            }
        }
    }
    // set values from the item existing
    if (item) {
        $scope.fieldCtgry = ctgry.category;
        $scope.itemTitle = item.item;
        $scope.itemImgUrl = item.img;
        console.log(item.fields);
        for (var k in item.fields) {
            if (item.fields.hasOwnProperty(k)) {
                $scope.fields.push({ name: k, value: item.fields[k] });
            }
        }
        $scope.action = "Edit";
    }
    // add a row whenever this button is called
    $scope.addNewChoice = function() {
        $scope.fields.push({ name: 'Field Name', value: '' });
    };

    $scope.createItem = function() {
        var flddata = {
            category: $scope.fieldCtgry,
            itemName: $scope.itemTitle,
            imgurl: $scope.itemImgUrl
        };
        flddata.fields = $scope.fields;

        $http.put('/item', flddata)
            .success(function(data, status, headers) {
                var msg = 'Mobile info added successfully!';
                if ($scope.action == 'edit') {
                    msg = 'Mobile info edited successfully!';
                }
                // intimate success
                $rootScope.alertMsg('success', msg);
                $location.path('/');
            })
            .error(function(data, status, headers, config) {
                $rootScope.alertMsg('danger', "Error while creating item" + data.error);
            });
    };
});