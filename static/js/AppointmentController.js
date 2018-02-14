function AppointmentController($http) {
	let vm = this;
	vm.makingAppointment = false;
	vm.appointments = [];
	vm.searchQuery = '';

	vm.makeAppointment = function() {
		if(!vm.makingAppointment)
			return false;
	};

	vm.getAppointments = function() {
		$http.post('/search', {
			params: {
				search: vm.searchQuery
			}
		}).then(function(data) {
			vm.appointments = data.data;
			vm.searchQuery = '';
		});
	};

	vm.getAppointments();
}