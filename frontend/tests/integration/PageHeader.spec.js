import { shallowMount, mount, createLocalVue } from '@vue/test-utils'
import VueRouter from 'vue-router'
import routes from "@/routes.js"
import PageHeader from "@/components/PageHeader.vue"
import CreateDataset from "@/views/dataset/CreateDataset.vue"

const localVue = createLocalVue()
localVue.use(VueRouter)

describe("PageHeader", () => {
  it("renders a child component via routing", () => {
    const router = new VueRouter({ routes })
    const wrapper = mount(PageHeader, { localVue, router })

    router.push("/datasets/create")

    expect(wrapper.find(CreateDataset).exists()).toBe(true)
  })
})
