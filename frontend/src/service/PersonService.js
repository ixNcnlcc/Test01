// services/PersonService.js
import axios from 'axios';

export default {
  fetchPersons() {
    return axios.get('/api/persons/');
  },
  deletePerson(id) {
    return axios.delete(`/api/persons/${id}/`);
  }
};