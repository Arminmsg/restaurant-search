<template>
  <main>
    <div class="page">
      <div class="page__container">
        <div class="search-bar">
          <div class="search-bar__container">
            <input
              v-model="query"
              @input="search"
              type="text"
              class="search-bar__input"
              placeholder="Search for Restaurants by Name, Cuisine, Location"
            />
          </div>
        </div>
        <div class="page__content">
          <div class="filter">
            <div @click="toggleFilterMenu" class="filter__header">
              <span class="filter__header-text">Filter</span>
            </div>
            <div class="filter__container" :class="{'filter__container--open': isFilterMenuVisible}">
              <div class="filter__section">
                <span class="filter__title">Cuisine/Food Type</span>
                <label
                  v-for="(count, foodType) in foodTypes"
                  :key="foodType"
                  @click="toogleFoodType(foodType)"
                  :class="{ 'filter__label--active': isFoodTypeActive(foodType) }"
                  class="filter__label">
                  <span class="filter__label-text">
                    {{ shorten(foodType) }}
                  </span>
                  <span class="filter__label-number">
                    {{ count }}
                  </span>
                </label>
              </div>
              <div class="filter__section">
                <span class="filter__title">Rating</span>
                <label class="filter__label">
                  <span class="filter__label-text">⭐</span>
                </label>
                <label class="filter__label">
                  <span class="filter__label-text">⭐⭐</span>
                </label>
                <label class="filter__label">
                  <span class="filter__label-text">⭐⭐⭐</span>
                </label>
                <label class="filter__label">
                  <span class="filter__label-text">⭐⭐⭐⭐</span>
                </label>
                <label class="filter__label">
                  <span class="filter__label-text">⭐⭐⭐⭐⭐</span>
                </label>
              </div>

              <div class="filter__section">
                <span class="filter__title">Payment Options</span>
                <label
                  v-for="(count, paymentOption) in paymentOptions"
                  :key="paymentOption"
                  @click="togglePaymentOption(paymentOption)"
                  :class="{ 'filter__label--active': isPaymentOptionActive(paymentOption) }"
                  class="filter__label"
                >
                  <span class="filter__label-text">
                    {{ shorten(paymentOption) }}
                  </span>
                </label>
              </div>
            </div>
          </div>
          <div class="results">
            <div :class="{ hidden: hits.length === 0 }">
              <div class="results__stats-bar">
                <span class="results__count-text"
                  ><span>
                    {{ numOfHits }} results found in {{ (1 / 1000) * processingTime }} seconds
                  </span></span
                >
              </div>
              <div v-for="hit in hits" :key="hit.objectID" class="results__item">
                <div class="result">
                  <div class="result__image-container">
                    <img class="result__image" :src="hit.image_url" alt="" />
                  </div>
                  <div class="result__text-container">
                    <h1 class="result__title">{{ hit.name }}</h1>
                    <p class="result__summary">
                      {{ hit.food_type }} | {{ hit.neighborhood }} | {{ hit.price_range }}
                    </p>
                  </div>
                </div>
              </div>

              <div class="button" v-if="!hasNoNextPage">
                <button href="#" v-on:click="getNextPage()" class="button__link">Show More</button>
              </div>
            </div>
            <div :class="{ hidden: hits.length >= 1 }" class="results__item">
              <p class="result__title">
                We didn't find any results for the search <em>"{{ query }}"</em>.
              </p>
              <span @click="clearSearch()" class="clear-all">Clear search</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import algoliasearch from 'algoliasearch'
import algoliasearchHelper from 'algoliasearch-helper'

export default {
  data() {
    return {
      query: '',
      location: null,
      error: null,
      hits: [],
      helper: null,
      numOfHits: '',
      processingTime: '',
      hasNoNextPage: false,
      foodTypes: [],
      paymentOptions: [],
      activeFilters: {
        foodTypes: [],
        paymentOptions: []
      },
      isFilterMenuVisible: false
    }
  },
  mounted() {
    // Initialize Algolia client and helper
    // Load as env vars, make it easier to test in different envs
    const applicationID = import.meta.env.VITE_APPLICATION_ID
    const apiKey = import.meta.env.VITE_API_KEY
    const indexName = import.meta.env.VITE_INDEX_NAME
    const client = algoliasearch(applicationID, apiKey)
    this.helper = algoliasearchHelper(client, indexName, {
      facets: ['food_type', 'payment_options'],
      disjunctiveFacets: ['food_type', 'payment_options']
    })

    // Handle the result event
    this.helper.on('result', this.handleResult)
    this.helper.on('error', (err) => console.log(err))

    // check if there is already a query param
    const urlParams = new URLSearchParams(window.location.search);
    const queryString = urlParams.get('query');

    if(queryString) {
      const queryParams = new URLSearchParams(queryString);
      queryParams.forEach((value, key) => {
        switch(key) {
          case "aroundLatLng":
            this.location = {
              latitude: value.split(",")[0],
              longitude: value.split(",")[1]
            }
            break;
          case "query":
            this.query = value
            break;
        }
      })

      this.search()

    } else {
      //Initial search to populate facets
      this.helper.search()
      this.helper.setPage(0)
      navigator.geolocation.getCurrentPosition(this.showPosition, this.showPositionError)
    }
  },
  methods: {
    showPosition(position) {
      this.location = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude
      }
      this.helper.setQueryParameter(
        'aroundLatLng',
        `${this.location.latitude},${this.location.longitude}`
      )
      this.search()
    },
    showPositionError(err) {
      // TODO display some kind of popup for the user
      fetch('https://ipapi.co/json/')
        .then((response) => response.json())
        .then((data) => {
          this.location = {
            latitude: data.latitude,
            longitude: data.longitude
          }
          this.helper.setQueryParameter(
            'aroundLatLng',
            `${this.location.latitude},${this.location.longitude}`
          )
          this.search()
        })
        .catch(() => {
          this.error = 'Failed to get location from IP API.'
        })
    },
    search() {
      this.hits = []
      this.helper.setPage(0)
      this.helper.setQuery(this.query).search()
    },
    handleResult(event) {
      this.hits = this.hits.concat(event.results.hits)
      this.numOfHits = event.results.nbHits
      this.processingTime = event.results.processingTimeMS
      this.numOfPages = event.results.nbPages
      this.hasNoNextPage = this.helper.getPage() >= this.numOfPages - 1 || this.numOfPages === 0

      // Add query params to the url to make it shareable
      const url = new URL(window.location);
      url.searchParams.set('query', event.results.params);
      window.history.pushState({}, '', url);

      if (this.foodTypes.length === 0) {
        this.foodTypes = event.results.facets[0].data
        Object.entries(this.foodTypes).forEach((x) => (this.activeFilters.foodTypes[x[0]] = false))
      } else {
        // Always display the full selection of cuisines
        for(let key in this.foodTypes) {
          this.foodTypes[key] = 0;
        }
        Object.entries(event.results.facets[0].data).forEach(([foodType, count]) => this.foodTypes[foodType] = count)
      }
      if (this.paymentOptions.length === 0) {
        let paymentOptionsResult = event.results.facets[1].data;
        ['Diners Club', 'Carte Blanche', 'JCB', 'Pay with OpenTable', 'Cash Only'].forEach(
          (key) => {
            // TODO make sure that the key exists before deleting
            delete paymentOptionsResult[key]
          }
        )
        this.paymentOptions = paymentOptionsResult
        Object.entries(this.paymentOptions).forEach(
          (x) => (this.activeFilters.paymentOptions[x[0]] = false)
        )
      }
    },
    getNextPage() {
      this.helper.nextPage()
      this.helper.search()
    },
    toogleFoodType(foodType) {
      this.hits = []
      this.helper.setPage(0)
      this.activeFilters.foodTypes[foodType] = !this.activeFilters.foodTypes[foodType]
      if (this.activeFilters.foodTypes[foodType]) {
        this.helper.addDisjunctiveFacetRefinement('food_type', foodType)
      } else {
        this.helper.removeDisjunctiveFacetRefinement('food_type', foodType)
      }
      this.search()
    },
    togglePaymentOption(paymentOption) {
      this.hits = []
      this.helper.setPage(0)
      let selectedPaymentOption = []

      if (paymentOption === 'Discover') {
        selectedPaymentOption = ['Diners Club', 'Carte Blanche', 'Discover']
      } else {
        selectedPaymentOption = [paymentOption]
      }

      selectedPaymentOption.forEach((x) => {
        this.activeFilters.paymentOptions[x] = !this.activeFilters.paymentOptions[x]
        if (this.activeFilters.paymentOptions[paymentOption]) {
          this.helper.addDisjunctiveFacetRefinement('payment_options', paymentOption)
        } else {
          this.helper.removeDisjunctiveFacetRefinement('payment_options', paymentOption)
        }
      })
      this.search()
    },
    isFoodTypeActive(foodType) {
      return this.activeFilters.foodTypes[foodType]
    },
    isPaymentOptionActive(paymentOption) {
      return this.activeFilters.paymentOptions[paymentOption]
    },
    shorten(text) {
      return text.length > 17 ? text.substring(0, 14) + '...' : text
    },
    clearSearch() {
      this.query = ''
      this.search()
    },
    toggleFilterMenu() {
      console.log("running")
      this.isFilterMenuVisible = !this.isFilterMenuVisible
    }
  }
}
</script>
