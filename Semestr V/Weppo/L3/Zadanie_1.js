const person = {name: "John",
                surname: "Nash",
                age: 22,
                set_age: function(new_age){
                    this.age = new_age},
                'get age': function(){
                    return this.age}}
// właściwości można dodać na dwa sposoby
person.latest_publication = "Equilibrium Points in N-person Games"
person["wife"] = "Alicia Lardé López-Harrison"
person['This will work'] = true
// person.'This will not work' = True


person.get_full_name = function(){return this.name + " " + this.surname}
person['set_latest_publication'] = function(name){this.latest_publication = name}
//person.'This will not work' = some function

console.log(person['get age']())
console.log(person.get_full_name())
person.set_latest_publication("The Bargaining Problem")
console.log(person.latest_publication)