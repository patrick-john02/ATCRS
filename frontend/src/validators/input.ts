import * as yup from 'yup'

export const loginSchema = yup.object({
    username: yup.string().required('username is required'),
    password: yup.string().required('password is required')
})

export const RegisterSchema = yup.object({
    first_name: yup.string().required('First name is required'),
    last_name: yup.string().required('Last name is required '),
    username: yup.string().required('Username is required'),
    email: yup.string().required('Email is required'),
    password: yup.string().required('Password is required'),
    birthdate: yup.string().required('Birdate is required'),
    contact_number: yup.string().required('Contact number is required'),
    address: yup.string().required('Address is required'),
    high_school: yup.string().required('Previous High School is required'),
    year_graduated: yup.string().required('Year Graduated is required'),
})

