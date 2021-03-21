<template>
	<div class='container'>
		<div class='row'>
			<div class='col-sm-12'>
				<h1>TODO lists</h1>
				<hr><br><br>
				<button type='button' class='btn btn-success btn-sm' v-b-modal.add-list-modal>Add list</button>
				<br><br>
				<alert :variant='alert.variant' :message='alert.message' v-if='alert.message'></alert>
				<table class='table table-hover'>
					<thead>
						<tr>
							<th scope='col'>Name</th>
							<th scope='col'>Todos</th>
							<th scope='col'>Date</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for='(list, index) in lists' :key='index' @click='gotoList(list, $event)'>
							<td>{{ list.name }}</td>
							<td>{{ list.todos.length }}</td>
							<td>---</td>
							<td>
								<div class='btn-group' role='group'>
									<button type='button' class='btn btn-warning btn-sm' v-b-modal.update-list-modal @click='initUpdateForm(list)'>Update</button>
									<button type='button' class='btn btn-danger btn-sm' @click='onDelete(list.id_list)'>Delete</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<b-modal ref='addListModal' id='add-list-modal' title='Add a TODO list' hide-footer>
			<b-form @submit='onAddSubmit' @reset='onAddReset' class='w-100'>
				<b-form-group id='form-title-group' label='Name:'>
					<b-form-input id='form' type='text' v-model='addListForm.name' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' variant='primary'>Submit</b-button>
				<b-button type='reset' variant='danger'>Reset</b-button>
			</b-form>
		</b-modal>

		<b-modal ref='updateListModal' id='update-list-modal' title='Update a TODO list' hide-footer>
			<b-form @submit='onUpdateSubmit' @reset='onUpdateReset' class='w-100'>
				<b-form-group id='form-title-group' label='Name:'>
					<b-form-input id='form' type='text' v-model='updateListForm.name' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' variant='primary'>Submit</b-button>
				<b-button type='reset' variant='danger'>Reset</b-button>
			</b-form>
		</b-modal>
	</div>
</template>

<script>
import axios from 'axios';
import Alert from '@/components/Alert.vue';
import BASE_URL from '@/config';

export default {
	data() {
		return {
			lists: [],
			addListForm: {
				name:''
			},
			updateListForm: {
				id_list: -1,
				name:''
			},
			alert: {
				message: '',
				variant: 'danger'
			}
		};
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
		getLists() {
			const path = `${BASE_URL}/lists`;
			this.handle(axios.get(path),
				res => {
					this.lists = res.data;
				},
				this.onError
			);
		},
		initAddForm() {
			this.addListForm.name = '';
		},
		initUpdateForm(list) {
			this.updateListForm.id_list = list.id_list;
			this.updateListForm.name = list.name;
		},
		onError(error) {
			this.alert.variant = 'danger';
			this.alert.message = error.message;
		},
		onSuccess(message) {
			this.getLists();
			this.alert.variant = 'success';
			this.alert.message = message;
		},
		onAddSubmit(evt) {
			evt.preventDefault();
			this.$refs.addListModal.hide();
			const path = `${BASE_URL}/lists`;
			this.handle(axios.put(path, this.addListForm),
				() => this.onSuccess('TODO list added'),
				this.onError
			);
			this.initAddForm();
		},
		onAddReset(evt) {
			evt.preventDefault();
			this.$refs.addListModal.hide();
			this.initAddForm();
		},
		onUpdateSubmit(evt) {
			evt.preventDefault();
			this.$refs.updateListModal.hide();
			const path = `${BASE_URL}/lists/${this.updateListForm.id_list}`;
			const payload = {
				name: this.updateListForm.name
			};
			this.handle(axios.patch(path, payload),
				() => this.onSuccess('TODO list updated'),
				this.onError
			);
		},
		onUpdateReset(evt) {
			evt.preventDefault();
			this.$refs.updateListModal.hide();
		},
		onDelete(id_list) {
			const path = `${BASE_URL}/lists/${id_list}`;
			this.handle(axios.delete(path),
				() => this.onSuccess('TODO list deleted'),
				this.onError
			);
		},
		gotoList(list, event) {
			if (event.target.tagName == 'TD') {
				this.$router.push(`list/${list.id_list}`);
			}
		}
	},
	components: {
		alert: Alert
	},
	beforeMount() {
		this.getLists();
	}
};

</script>
