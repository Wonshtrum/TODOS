<template>
  <div class='container'>
	<b-modal ref='signupModal' id='signup-modal' title='SignUp' no-close-on-esc no-close-on-backdrop hide-header-close hide-footer>
		<b-form @submit='onSubmit' class='w-100'>
			<alert :variant='"danger"' :message='message' v-if='message'></alert>
			<b-form-group id='form-user-group' label='Username:'>
				<b-form-input id='form' type='text' v-model='userForm.user' required>
				</b-form-input>
			</b-form-group>
			<b-form-group id='form-pwd-group' label='Password:'>
				<b-form-input id='form' type='password' v-model='userForm.pwd' required>
				</b-form-input>
			</b-form-group>
			<b-button type='submit' variant='primary'>Submit</b-button>
			<router-link to='/login' variant='primary' tag='b-button'>Login</router-link>
		</b-form>
	</b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from '@/components/Alert.vue';
import { AUTH_REQUEST } from '@/store/actions';
import BASE_URL from '@/config';

export default {
	data() {
		return {
			userForm: {
				user: '',
				pwd: ''
			},
			message: ''
		}
	},
	methods: {
		handle(request, onSuccess, onError) {
			request.then(res => {
				if (res.data.status == 0) {
					onSuccess(res.data);
					return;
				}
				onError(res.data);
			}).catch(error => {
				onError(error.response.data);
			});
		},
		login() {
			this.$store.dispatch(AUTH_REQUEST, this.userForm).then(() => {
				this.$router.push('/');
			}).catch(error => {
				this.message = error.message;
			});
		},
		onSubmit(evt) {
			evt.preventDefault();
			const path = `${BASE_URL}/account`;
			this.handle(axios.post(path, this.userForm),
				this.login,
				error => { this.message = error.message; }
			);
		}
	},
	mounted() {
		this.$refs.signupModal.show();
	},
	components: {
		alert: Alert
	}
}

</script>
