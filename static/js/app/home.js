/**
 * Created by Jhonsson on 18/05/15.
 */

    $(document).ready(function(){
         window.location.assign('#/');
    });
    angular.module("sico_ia", ['ngRoute', 'ngAnimate', 'ngSanitize'])


    .controller('error', ['$scope', function($scope){
    }])

    .controller('home', ['$scope', function($scope){
    }])


    .controller('AppCtrl', ['$scope', function($scope) {

        $scope.logout=function(){
            window.location.assign('/salir');
        };
        $scope.menuLateral=[];
        $scope.sidebar=function(opciones, seleccion){

            $scope.menuLateral=opciones;
            if (opciones.length > 0 && seleccion.length > 0)
                $scope.seleccion(seleccion);
        };
        $scope.menuMovil={
            'menu':false,
            'sidebar':false
        };
        $scope.seleccion=function(seleccion){

            if($scope.menuLateral.length > 0){
                for (var i=0; i<$scope.menuLateral.length; i++) {
                    if (seleccion != $scope.menuLateral[i].link){
                        $scope.menuLateral[i].activo=false;
                    }else{
                        $scope.menuLateral[i].activo=true;
                        $scope.criterio =  $scope.menuLateral[i].link;
                    }
                }

            }

        };

        $scope.modulos = {{modulos|safe}};

    }])






    .controller('enconstruccion', ['$scope', function($scope){

        $scope.cerrarDlg=function(){
              window.location.assign('#/');
        };

    }])







    .controller('busquedas', ['$scope', '$http', '$templateCache',
    function($scope, $http){

        $scope.iString=function(valu){
            return angular.isString(valu);
        };

        $scope.buscarPost=function(){
             $scope.buscando=true;
             $scope.valores ={};
             $http(
                 {
                     method: 'POST',
                     url: "{% url 'busquedacriterio' %}",
                     data: {
                        'formulario': $('#buscarForm').serialize()
                     }
                 }
             )
             .success(function(data) {
                     //console.log(data);
                     $scope.valores = data;
                     $scope.buscando=false;
                 }
             )
             .error(function(data) {
                     $scope.valores = data || "Request failed";
                     $scope.buscando=false;
                     $scope.valores ={}
                 }
             );
        };

        $scope.medidorSeleccionado=-1;

        $scope.seleccionDeMedidor=function(indice){
            console.log(indice);
            $scope.medidorSeleccionado=indice;
        };

        $scope.getAttributeByIndex =function (obj, index){
            var i = 0;
            for (var attr in obj){
                if (index === i){
                    return {
                        key: attr,
                        value: obj[attr]
                    };
                }
                i++;
            }
            return null;
        };

    }])



    .controller('cambiosdemedidor', ['$scope', function($scope){

        $scope.cuenta="";

    }])





    .directive('showFocus', function($timeout) {
      return function(scope, element, attrs) {
        scope.$watch(attrs.showFocus,
          function (newValue) {
            $timeout(function() {
                newValue && element.focus();
            });
          },true);
      };
    })

    .config( ['$routeProvider',
        function($routeProvider) {
            $routeProvider.when('/', {
                controller: 'home',
                templateUrl: "{% url 'principal' %}"
            }).
            when('/espera', {
                templateUrl: "{% url 'espera' %}"
            }).
            when('/error', {
                controller: 'error',
                templateUrl: "{% url 'error' %}"
            }).
            when('/cambiosdemedidor', {
                controller: 'cambiosdemedidor',
                templateUrl: "{% url 'cambiosdemedidor' %}"
            }).
            when('/porcuenta', {
                controller: 'busquedas',
                templateUrl: "{% url 'busquedas' %}"
            }).
            when('/pormedidor', {
                controller: 'busquedas',
                templateUrl: "{% url 'busquedas' %}"
            }).
            when('/pornombre', {
                controller: 'busquedas',
                templateUrl: "{% url 'busquedas' %}"
            }).
            when('/porgeocodigo', {
                controller: 'busquedas',
                templateUrl: "{% url 'busquedas' %}"
            }).

            when('/salir', {
                templateUrl: "{% url 'salir' %}"
            }).
            when('/enconstruccion', {
                controller: 'enconstruccion',
                templateUrl: "{% url 'enconstruccion' %}"
            }).
            otherwise({
              redirectTo: '/enconstruccion'
            })
            ;
      }])

    .config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);


