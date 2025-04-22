from django.db.models import Model, CharField, IntegerField, ForeignKey, SET_NULL, BooleanField, ImageField, DateField, \
    CASCADE, ManyToManyField


class Picture(Model):
    img = ImageField(upload_to="pictures/car_pictures/", null=False, blank=True)


# creating models of cars which are linked with each unique car in database
class CarModel(Model):
    name = CharField(max_length=50, null=False, blank=False, unique=True)
    c_for = IntegerField(null=False, blank=False) # c_for or car_field_of_range. The amount of km per charge in a model
    description = CharField(max_length=200, null=True, blank=True)
    num_seats = IntegerField(null=False, blank=False)
    pictures = ManyToManyField(Picture) # set of images showcasing the model

    class Meta:
        ordering = ('name', 'num_seats', 'c_for')

    def __str__(self):
        return f"car model {self.name} with {self.num_seats} seats and {self.c_for}km of range"

    def __repr__(self):
        return (f"model: {self.name} \n"
                f"range: {self.c_for}km")


class CarColor(Model):
    name = CharField(max_length=25, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"color: {self.name}"

    def __repr__(self):
        return f"color: {self.name}"


# establishes individual cars in the database
class Car(Model):
    model = ForeignKey(CarModel, null=False, blank=False, on_delete=CASCADE, related_name='cars')
    transmission = BooleanField(null=False, blank=False, default=False) # false for manual, true for auto
    color = ForeignKey(CarColor, null=False, blank=False, on_delete=CASCADE, related_name='cars') # linked with color db
    established = DateField(null=False, blank=False, auto_now_add=True) # when was the car put in the salon
    price = IntegerField(null=False, blank=False, default=0)
    designation = BooleanField(null=False, blank=False, default=False) # for_sale = true, for_rent = false
    test_drive = BooleanField(null=False, blank=False, default=False)
    cid = CharField(max_length=16, null=False, blank=False, unique=True) # SPZ or car id, unique set of characters for identification
    location = CharField(max_length=50, null=False, blank=False, unique=False) # city of the cars location

    class Meta:
        ordering = ['cid' ,'established'] # orders the db by the SPZ and by the date when the car was taken in the shop

    def __str__(self):
        return f"this car is of model {self.model.name}, id {self.cid} and was established {self.established}"

    def __repr__(self):
        return (f"model: {self.model.name} \n"
                f"id {self.cid} \n"
                f"established: {self.established}")



