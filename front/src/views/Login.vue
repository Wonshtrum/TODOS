<template>
  <div class='container'>
	<b-modal ref='loginModal' id='login-modal' title='Login' no-close-on-esc no-close-on-backdrop hide-header-close hide-footer>
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
			<router-link to='/signup' variant='primary' tag='b-button'>SignUp</router-link>
		</b-form>
	</b-modal>
  </div>
</template>

<script>
import { AUTH_REQUEST } from '@/store/actions';
import Alert from '@/components/Alert.vue';

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
		onSubmit(evt) {
			evt.preventDefault();
			this.$store.dispatch(AUTH_REQUEST, this.userForm).then(() => {
				this.$router.push('/');
			}).catch(error => {
				this.message = error.message;
			});
		}
	},
	mounted() {
		this.$refs.loginModal.show();
	},
	components: {
		alert: Alert
	}
}

</script>
