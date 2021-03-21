<template>
	<div class='container'>
		<div class='row'>
			<div class='col-sm-12'>
				<h1>{{ name }}</h1>
				<hr><br><br>
				<button type='button' class='btn btn-success btn-sm' v-b-modal.add-todo-modal>Add TODO</button>
				<br><br>
				<alert :variant='alert.variant' :message='alert.message' v-if='alert.message'></alert>
				<table class='table table-hover'>
					<thead>
						<tr>
							<th scope='col'>Name</th>
							<th scope='col'>Task</th>
							<th scope='col'>Date</th>
							<th></th>
						</tr>
					</thead>
					<tbody>
						<tr v-for='(todo, index) in todos' :key='index'>
							<td>{{ todo.name }}</td>
							<td>{{ todo.task }}</td>
							<td>{{ todo.date }}</td>
							<td>
								<div class='btn-group' role='group'>
									<button type='button' class='btn btn-warning btn-sm' v-b-modal.update-todo-modal @click='initUpdateForm(todo)'>Update</button>
									<button type='button' class='btn btn-danger btn-sm' @click='onDelete(todo.id_todo)'>Delete</button>
								</div>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>

		<b-modal ref='addTodoModal' id='add-todo-modal' title='Add a TODO' hide-footer>
			<b-form @submit='onAddSubmit' @reset='onAddReset' class='w-100'>
				<b-form-group id='form-name-group' label='Name:'>
					<b-form-input id='form' type='text' v-model='addTodoForm.name' required>
					</b-form-input>
				</b-form-group>
				<b-form-group id='form-task-group' label='Task:'>
					<b-form-input id='form' type='text' v-model='addTodoForm.task' required>
					</b-form-input>
				</b-form-group>
				<b-button type='submit' variant='primary'>Submit</b-button>
				<b-button type='reset' variant='danger'>Reset</b-button>
			</b-form>
		</b-modal>

		<b-modal ref='updateTodoModal' id='update-todo-modal' title='Update a TODO' hide-footer>
			<b-form @submit='onUpdateSubmit' @reset='onUpdateReset' class='w-100'>
				<b-form-group id='form-name-group' label='Name:'>
					<b-form-input id='form' type='text' v-model='updateTodoForm.name' required>
					</b-form-input>
				</b-form-group>
				<b-form-group id='form-task-group' label='Task:'>
					<b-form-input id='form' type='text' v-model='updateTodoForm.task' required>
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
import Alert from '@/components/Alert.vue'
import BASE_URL from '@/config'

export default {
	data() {
		return {
			name: 'Loading...',
			todos: [],
			addTodoForm: {
				name:'',
				task:''
			},
			updateTodoForm: {
				id_todo: -1,
				name:'',
				task:''
			},
			id_list: this.$route.params.id_list,
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
		initAddForm() {
			this.addTodoForm.name = '';
			this.addTodoForm.task = '';
		},
		initUpdateForm(todo) {
			this.updateTodoForm.id_todo = todo.id_todo;
			this.updateTodoForm.name = todo.name;
			this.updateTodoForm.task = todo.task;
		},
		getTodos() {
			const path = `${BASE_URL}/lists/${this.id_list}`;
			this.handle(axios.get(path),
				res => {
					this.todos = res.data.todos;
					this.name = res.data.name;
				},
				this.onError
			);
		},
		onError(error) {
			this.alert.variant = 'danger';
			this.alert.message = error.message;
		},
		onSuccess(message) {
			this.getTodos();
			this.alert.variant = 'success';
			this.alert.message = message;
		},
		onAddSubmit(evt) {
			evt.preventDefault();
			this.$refs.addTodoModal.hide();
			const path = `${BASE_URL}/lists/todos/${this.id_list}`;
			this.handle(axios.put(path, this.addTodoForm),
				() => this.onSuccess('TODO added'),
				this.onError
			);
			this.initAddForm();
		},
		onAddReset(evt) {
			evt.preventDefault();
			this.$refs.addTodoModal.hide();
			this.initAddForm();
		},
		onUpdateSubmit(evt) {
			evt.preventDefault();
			this.$refs.updateTodoModal.hide();
			const path = `${BASE_URL}/lists/todos/${this.id_list}/${this.updateTodoForm.id_todo}`;
			const payload = {
				name: this.updateTodoForm.name,
				task: this.updateTodoForm.task,
			};
			this.handle(axios.patch(path, payload),
				() => this.onSuccess('TODO updated'),
				this.onError
			);
		},
		onUpdateReset(evt) {
			evt.preventDefault();
			this.$refs.updateTodoModal.hide();
			this.initUpdateForm();
		},
		onDelete(id_todo) {
			const path = `${BASE_URL}/lists/todos/${this.id_list}/${id_todo}`;
			this.handle(axios.delete(path),
				() => this.onSuccess('TODO deleted'),
				this.onError
			);
		}
	},
	components: {
		alert: Alert
	},
	beforeMount() {
		this.getTodos();
	}
};

</script>
