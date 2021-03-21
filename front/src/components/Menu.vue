<template>
	<b-navbar toggleable="lg" type="dark" variant="info">
		<b-navbar-brand href="/">TODOS®</b-navbar-brand>
		<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

		<b-collapse id="nav-collapse" is-nav>
			<b-navbar-nav>
				<router-link to='/' tag='b-nav-item'>Home</router-link>
				<router-link to='/login' tag='b-nav-item' v-if='!$store.getters.isAuthenticated'>Login</router-link>
				<b-nav-item @click='disconnect' v-if='$store.getters.isAuthenticated'>Logout</b-nav-item>
			</b-navbar-nav>
			<b-navbar-nav class="ml-auto">
				<b-nav-item>{{$store.getters.user}}</b-nav-item>
			</b-navbar-nav>
		</b-collapse>
	</b-navbar>
</template>

<script>
import {AUTH_LOGOUT} from '@/store/actions';

export default {
	methods: {
		disconnect() {
			this.$store.dispatch(AUTH_LOGOUT);
			this.$router.push('/login');
		}
	}
}
</script>
