<template>
  <div id="app">

  <div class="demo-input-label"> 
    <el-input
      placeholder="1"
      v-model="price_weight"
      clearable>
       <template #prepend>价格权重：</template>
    </el-input>
  </div>

  <div class="demo-input-label">
    <el-input
      placeholder="1"
      v-model="over_weight"
      clearable>
      <template #prepend>溢价率权重:</template>
    </el-input>
  </div>

  <div class="demo-input-label">
    <el-input
      placeholder="0.5"
      v-model="return_weight"
      clearable>
      <template #prepend>到期收益率权重:</template>
    </el-input>
  </div>

  <div class="demo-input-label">
    <el-input
      placeholder="20"
      v-model="top_nums"
      clearable>
      <template #prepend>展示数量:</template>
    </el-input>
  </div>

  <el-button  @click="getStocks" type="primary" round> 提交</el-button>
  <p></p>
 
    <el-table
      :data="stockList"
      stripe
      border
      style="width: 100%">
      <el-table-column
        prop="rank"
        label="排名"
        width = 50>
      </el-table-column>
      <el-table-column
        prop="name"
        label="名称">
      </el-table-column>
      <el-table-column
        prop="code"
        label="代码">
      </el-table-column>
      <el-table-column
        prop="price"
        label="收盘价">
      </el-table-column>
      <el-table-column
        prop="score"
        label="打分">
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
import {onMounted ,ref} from "vue";
import { getCurrentInstance } from 'vue'

export default {
    name: 'App',
    setup() {
          const price_weight = ref(1);
          const over_weight = ref(1);
          const return_weight = ref(0.5);
          const top_nums = ref(20);
          const stockList = ref([]);

          const internalInstance = getCurrentInstance()
          const axios =internalInstance.appContext.config.globalProperties.axios;

          const getStocksHelper = async () => {
              getStocks()
          }
    
          function getStocks(){
            let api = "http://www.tenyunnet.cn/getStocks?over_weight=" + over_weight.value + "&price_weight=" + price_weight.value + "&return_weight=" + return_weight.value + "&top_nums=" + top_nums.value
            axios({
              methods: "get",
              url : api, 
              headers: {
                  'Content-type': 'application/json;charset=UTF-8'
              }
            })
            .then(res => {
                  console.log(res)
                  console.log(typeof(res.data))
                  console.log(res.data)
                  stockList.value = res.data

            })
          }
          onMounted(getStocksHelper)

          return {
            price_weight,
            over_weight,
            return_weight,
            top_nums,
            stockList,
            getStocks,
          }
      }
}

</script>>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

  .demo-input-label {
    width: 300px;
    padding: 10px;
    align-content: center;
  }

</style>
