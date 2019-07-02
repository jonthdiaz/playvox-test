Vue.component('template-app', {
  template: '#template-script',
	data(){
		return{
			search: "",
			users: [],
      notes: []
		}
	},
	methods:{
		search_users(value){
			var self = this
			fetch(`http://192.168.99.100:8010/v1/users/search_by?query=${self.search}`)
			.then(response => response.json())
			.then(data => {
			  self.users = data
			})
			.catch(error => console.error(error))
		},
    search_user_notes(user){
      var self = this
			fetch(`http://192.168.99.100:8011/v1/user/${user._id.$oid}/notes`)
			.then(response => response.json())
			.then(data => {
        self.notes.push(user._id.$oid)
        self.notes[user._id.$oid] = data
			})
			.catch(error => console.error(error))
    }
	}
})

new Vue({
	el: '#app',
	data(){
		return{

		}
	},
	mounted(){
	},
	})
