import { shallowMount } from '@vue/test-utils' // be sure to skip a line to avoid unit testing error

import ModelMultiSelect from '@/components/tags/ModelMultiSelect.vue'

let wrapper = null

beforeEach(() => {
    wrapper = shallowMount(ModelMultiSelect, {
        propsData: {
            models: [
                {
                    category: "tasks",
                    datasets: [],
                    name: "testing",
                    id: "5"
                }
            ]
        }
    })
})

afterEach(() => {
    wrapper.destroy()
})

describe('ModelMultiSelect', () => {
    describe(':initial state', () => {
        it('isHidden: filtered-list should be hidden', () => {
            let filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)
            expect(filtered_list.classes()).toContain('hidden')
        })

        it('filtered-list and selected-list initialized correctly', () => {
            wrapper.setProps({
                models: [
                    {
                        category: "tasks",
                        name: "test 1",
                        id: "5"
                    },
                    {
                        category: "tasks",
                        name: "test 2",
                        id: "6"
                    }
                ],
                currentTags: [
                    {
                        category: "tasks",
                        name: "test 3",
                        id: "1"
                    }
                ]
            })
            let filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)
            expect(filtered_list.findAll('li').length).toEqual(2)
            let selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
            expect(selected_list.findAll('li').length).toEqual(1)
        })
    })

    describe('@events', () => {
        it('focus on text box: removes `hidden` class on filtered-list', () => {
            const text = wrapper.findAll('[data-test-id="text"]').at(0)
            const filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)

            expect(filtered_list.classes()).toContain('hidden')
            text.trigger('focus')
            expect(filtered_list.classes()).not.toContain('hidden')
        })

        // NOT FINISHED. find a way to trigger vue-on-clickaway
        it('clickaway from box: adds `hidden` class on filtered-list', () => {
            const text = wrapper.findAll('[data-test-id="text"]').at(0)
            const filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)

            text.trigger('focus')
            expect(filtered_list.classes()).not.toContain('hidden')
            // text.trigger('clickaway')
            // expect(filtered_list.classes()).toContain('hidden')
            // expect(wrapper.element).toMatchSnapshot()
        })

        it('clicking tag on filteredTags adds tag to selectedTags', () => {
            // First check that filtered-list is populated and selected-list is not
            let filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)

            // Select (click) the tag from the filtered list
            let filtered_tag = filtered_list.findAll('li').at(0).find('div')
            expect(wrapper.element).toMatchSnapshot()
            filtered_tag.trigger('click')
            expect(wrapper.element).toMatchSnapshot()

            // Check that filtered-list is now empty and selected-list is populated
            let selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
            expect(selected_list.findAll('li').length).toEqual(1)

            filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)
            expect(filtered_list.findAll('li').length).toEqual(0)
        })

        it('clicking tag in selectedTags removes tag from selectedTags', () => {
            wrapper.setProps({
                models: [],
                currentTags: [
                    {
                        category: "tasks",
                        datasets: [],
                        name: "Airplane",
                        id: "7"
                    }
                ]
            })
            // filtered-list should be empty, and selectedTags should have one
            let filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)
            expect(filtered_list.findAll('li').length).toEqual(0)

            let selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
            expect(selected_list.findAll('li').length).toEqual(1)

            // click selected tag
            let selected_tag = selected_list.findAll('li').at(0).find('div')
            expect(wrapper.element).toMatchSnapshot()
            selected_tag.trigger('click')
            expect(wrapper.element).toMatchSnapshot()

            // Check that selected-list is now empty. The tag should be in removed_tags
            selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
            expect(selected_list.findAll('li').length).toEqual(0)
        })

        describe('@enter a word in text box', () => {
            it('create new tag', () => {
                wrapper.setProps({ createNew: true })
                wrapper.setData({query: 'birds'})
                let selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
                expect(selected_list.findAll('li').length).toEqual(0)

                expect(wrapper.element).toMatchSnapshot()
                const text = wrapper.findAll('[data-test-id="text"]').at(0)
                text.trigger('keydown.enter')
                expect(wrapper.element).toMatchSnapshot()

                selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
                expect(selected_list.findAll('li').length).toEqual(1)
            })

            it('select existing tag', () => {
                wrapper.setData({query: 'testing'})

                const text = wrapper.findAll('[data-test-id="text"]').at(0)
                text.trigger('keydown.enter')

                let filtered_list = wrapper.findAll('[data-test-id="filtered-list"]').at(0)
                expect(filtered_list.findAll('li').length).toEqual(0)
                let selected_list = wrapper.findAll('[data-test-id="selected-list"]').at(0)
                expect(selected_list.findAll('li').length).toEqual(1)
            })
        })
    })
})