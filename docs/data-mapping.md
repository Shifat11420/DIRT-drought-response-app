# Drought Response - Data Flow

## Inputs - App to API

### Add Field

- Name
- Location
  - ZipCode
  - Coords
    - Lat
    - Lon
- Acreage
- CropType
- SoilType
- HydrologicGroup
- PlantDate
- FieldId (auto | PK)

#### Full request body example

```json
{
  "cropType": "Cotton",
  "soilType": "Sandy loam",
  "initMoistCond": "Really Wet",
  "hydroSoilGrp": "D",
  "plantCond": "Poor Drainage",
  "plantDate": "5/11/2016",
  "fieldSize": 0.26018,
  "seasonLength": 162,
  "fieldCap": 0.46,
  "permWiltPoint": 0.4,
  "maxAllowDepl": "",
  "maxRootDepth": ""
}
```

#### Mapping inputs to request parameters

| InputName       | Request FieldName |
| --------------- | ----------------- |
| Location        | ???               |
| Acreage         | fieldSize         |
| CropType        | cropType          |
| SoilType        | soilType          |
| HydrologicGroup | hydroSoilGrp      |
| PlantDate       | plantDate         |

#### Unused request parameters

- "initMoistCond": "Really Wet",
  - Add to user inputs
- "plantCond": "Poor Drainage",
  - from hydrological group
- "seasonLength": 162,
  - from crop
- "fieldCap": 0.46,
  - from soiltype
- "permWiltPoint": 0.4,
  - from soiltype
- "maxAllowDepl": "",
  - from crop
- "maxRootDepth": ""
  - from crop

---

add all request as overridable inputs on the field screen

---

To make model/schema changes
Update in models.py and then run:

```python
python manage.py makemigrations
python manage.py migrate
```

---

database updates at settings.py
