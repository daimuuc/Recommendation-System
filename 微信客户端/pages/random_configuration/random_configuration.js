// pages/random_configuration/random_configuration.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   *确认按钮函数,保存数据,
   *跳转界面 
   */
  confirm: function (e) {
    //保存数据
    var val = e.detail.value
    console.log(val)
    app.globalData.random_configuration = val

    //获取随机生成文件参数配置
    var random_configuration = app.globalData.random_configuration
    //获取推荐参数配置
    var recommend_configuration = app.globalData.recommend_configuration
    //参数配置
    var configuration = {}
    for (var k in random_configuration) {
      configuration[k] = random_configuration[k]
    }
    for (var k in recommend_configuration) {
      configuration[k] = recommend_configuration[k]
    }
    console.log(configuration)

    wx.showLoading({
      title: '处理中,请耐心等待',
      mask: true
    })
    //请求接口处理并以json格式返回结果
    wx.request({
      url: 'https://www.ponma.cn:5000/random', // 接口地址
      data: configuration,
      header: {
        'content-type': 'application/json' // 默认值
      },
      success(res) {
        console.log(res.data)
        //保存结果
        app.globalData.result = res.data
        wx.hideLoading()
        
        //界面跳转
        wx.navigateTo({
          url: '/pages/recommedation/recommedation'
        })
      },
      fail(err) {
        wx.hideLoading()
        wx.showToast({
          title: '处理失败',
          icon: 'none',
          duration: 2000
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})