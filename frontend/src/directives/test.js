// Creates the v-test directive

// v-test directive is used to uniquely identify DOM elements
// when testing without clogging the code with unused variables during production.

// Usage:
//      Just type in `v-test={ id: `name` }` and if you inspect the element
//      you not see the 'data-test-{name}', but when you run tests the variable
//      will be available.

export default (el, binding) => {
    if (process.env.NODE_ENV === 'test') {
        Object.keys(binding.value).forEach(value => {
            el.setAttribute(`data-test-${value}`, binding.value[value])
        })
    }
}