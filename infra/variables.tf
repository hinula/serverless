variable "region" {
  type    = string
  default = "eu-central-1"
}

variable "function_name" {
  type    = string
  default = "my-first-serverless-function"
}

variable "lambda_filename" {
  type    = string
  default = "../src/function.zip"
}

variable "environment_vars" {
  type = map(string)
  default = {
    OPENWEATHER_API_KEY = "" # terraform apply sırasında doldur (veya Actions pipeline ile)
  }
}
