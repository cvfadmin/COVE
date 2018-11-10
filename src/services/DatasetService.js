import Api from '@/services/Api'

export default {
    getDatasets () {
        return Api().get('/datasets')
    },

    getDatasetById (dataset_id) {
        return Api().get('/datasets/' + dataset_id)
    }
}