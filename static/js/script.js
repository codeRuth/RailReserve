var auth = new Vue({
  el: '#auth',
  data: {
    username: '',
    password: '',
    user: '',
    pass: ''
  },
  methods: {
    login: function () {
      var self = this
      axios.post('/login', {
          username: this.username,
          password: this.password
        })
        .then(function (response) {
          console.log(response.data)
          console.log(response.data.user)
          if (response.data.res === 'success') {
            self.setCookie("user", response.data.user, 7)
            window.location = '/home'
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    register: function () {
      axios.post('/register', {
          username: this.user,
          password: this.pass
        })
        .then(function (response) {
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setCookie: function (cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
      var expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }
  }
})

var home = new Vue({
  el: '#home',
  data: {
    src: '',
    dest: '',
    date: '2018-05-25',
    trains_data: [],
    ticket_data: [],
    showModal: false,
    modalData: {
      date: '',
      train: '',
      status: ''
    },
    ticketView: true
  },
  computed: {
    getUsername: function () {
      return this.getCookie('user')
    }
  },
  methods: {
    getCookie: function(cname) {
      var name = cname + "=";
      var decodedCookie = decodeURIComponent(document.cookie);
      var ca = decodedCookie.split(';');
      for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    },
    trains: function () {
      var self = this
      axios.post('/trains', {
          source: this.src,
          destination: this.dest
        })
        .then(function (response) {
          console.log(response.data.res)
          self.trains_data = response.data.res
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    reserve: function (user, train, date) {
      var self = this
      axios.post('/reserve', {
          user: user,
          train: train,
          date: date
        })
        .then(function (response) {
          self.showModal = true
          self.modalData.date = response.data.date
          self.modalData.train = response.data.train
          self.modalData.status = response.data.res
          console.log(response.data)
          //self.trains_data = response.data.res
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    setCookie: function (cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
      var expires = "expires=" + d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
    logout() {
      setCookie('user', '', 7)
      window.location = '/'
    },
    view: function (user, train, date) {
      var self = this
      axios.post('/view', {
          username: self.getCookie('user'),
        })
        .then(function (response) {
          console.log(response.data)
          self.ticket_data = response.data.res
          //self.trains_data = response.data.res
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    cancel:  function (user, train, date) {
      var self = this
      axios.post('/cancel', {
          user: user,
          pnr: pnr
        })
        .then(function (response) {
          // self.showModal = true
          // self.modalData.date = response.data.date
          // self.modalData.train = response.data.train
          // self.modalData.status = response.data.res
          // console.log(response.data)
          //self.trains_data = response.data.res
        })
        .catch(function (error) {
          console.log(error);
        });
    }
  }
})

function checkCookie() {
  var username = getCookie("username");
  if (username != "") {
    alert("Welcome again " + username);
  } else {
    username = prompt("Please enter your name:", "");
    if (username != "" && username != null) {
      setCookie("username", username, 365);
    }
  }
}