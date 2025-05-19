# 后端全部接口

postman储存如下:


```json
{
	"info": {
		"_postman_id": "98a0c57f-6644-4c5b-b766-764997758974",
		"name": "E-DBA",
		"description": "教育数据湾区(E-DBA)系统 - 为高等教育机构提供安全、透明、互操作的数据共享平台",
		"schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json",
		"_exporter_id": "44453662"
	},
	"item": [
		{
			"name": "api/v1",
			"item": [
				{
					"name": "auth",
					"item": [
						{
							"name": "Login Access Token",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/x-www-form-urlencoded"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": [
										{
											"key": "username",
											"value": "xyz@tech.org",
											"description": "(Required) "
										},
										{
											"key": "password",
											"value": "Str0ngP@ssw0rd!",
											"description": "(Required) "
										},
										{
											"key": "grant_type",
											"value": "password"
										},
										{
											"key": "scope",
											"value": ""
										},
										{
											"key": "client_id",
											"value": "password"
										},
										{
											"key": "client_secret",
											"value": "password"
										}
									]
								
                                "name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "<string>"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "<string>"
												},
												{
													"key": "client_secret",
													"value": "<string>"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"access_token\": \"<string>\",\n  \"token_type\": \"<string>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "<string>",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "<string>"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "<string>"
												},
												{
													"key": "client_secret",
													"value": "<string>"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "E-admin",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/x-www-form-urlencoded"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "eadmin@edba.com",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "eadmin@123",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "password"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "password"
												},
												{
													"key": "client_secret",
													"value": "password"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "O-convener",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/x-www-form-urlencoded"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "xyz@tech.org",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "Str0ngP@ssw0rd!",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "password"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "password"
												},
												{
													"key": "client_secret",
													"value": "password"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "Senior E-admin",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/x-www-form-urlencoded"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "senior@edba.com",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "SeniorEAdmin@123",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "password"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "password"
												},
												{
													"key": "client_secret",
													"value": "password"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "T-admin",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/x-www-form-urlencoded"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "urlencoded",
											"urlencoded": [
												{
													"key": "username",
													"value": "tadmin@edba.com",
													"description": "(Required) "
												},
												{
													"key": "password",
													"value": "TAdmin@123",
													"description": "(Required) "
												},
												{
													"key": "grant_type",
													"value": "password"
												},
												{
													"key": "scope",
													"value": ""
												},
												{
													"key": "client_id",
													"value": "password"
												},
												{
													"key": "client_secret",
													"value": "password"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/auth/login"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Register User",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/auth/register",
								"description": "注册新用户（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "O-convener Register Data Users",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json",
												"type": "text"
											},
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY3MTEzOTEsInN1YiI6IjgifQ.GV0duIaRN0ZY6-8ZbzXw2i4fSA7RbGIXOx31_WnBlds",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"datauser3@yourorg.com\",\n  \"username\": \"datauser1\",\n  \"password\": \"StrongPassw0rd!\",\n  \"permission_level\": 1\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Register O Convener",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "urlencoded",
									"urlencoded": []
								},
								"url": "{{baseUrl}}/api/v1/auth/register-o-convener",
								"description": "注册组织协调人(O-Convener)并创建组织"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"user_in\": {\n    \"email\": \"<email>\",\n    \"password\": \"<string>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\"\n  },\n  \"organization_in\": {\n    \"name\": \"<string>\",\n    \"description\": \"<string>\",\n    \"email_domain\": \"<string>\",\n    \"verification_document\": \"<string>\"\n  }\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register-o-convener"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"user_in\": {\n    \"email\": \"<email>\",\n    \"password\": \"<string>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\"\n  },\n  \"organization_in\": {\n    \"name\": \"<string>\",\n    \"description\": \"<string>\",\n    \"email_domain\": \"<string>\",\n    \"verification_document\": \"<string>\"\n  }\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register-o-convener"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "O-convener Register",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "  {\n    \"user_in\": {\n      \"email\": \"demo@email.io\",\n      \"username\": \"demouser\",\n      \"password\": \"Pass1234!\",\n      \"permission_level\": 0\n    },\n    \"organization_in\": {\n      \"name\": \"示例组织A\",\n      \"description\": \"这是一个演示用的组织描述。\",\n      \"email_domain\": \"example.demo.org\",\n      \"verification_document\": \"dummy_base64_string_for_test\"\n    }\n  }",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/register-o-convener"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Reset Password",
							"request": {
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "<string>",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/auth/password-reset",
								"description": "密码重置（发送重置链接到邮箱）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "<string>",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/password-reset"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"msg\": \"<string>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "<string>",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/auth/password-reset"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Test Token",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": "{{baseUrl}}/api/v1/auth/test-token",
								"description": "测试访问令牌"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": "{{baseUrl}}/api/v1/auth/test-token"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
								},
								{
									"name": "Test O-convener token",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											},
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTc5OTIsInN1YiI6IjgifQ.VRehD9y5dCZkOu8aFBen5x4omrDkcegRcN4NmiGH9JY",
												"type": "text"
											}
										],
										"url": "{{baseUrl}}/api/v1/auth/test-token"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "{{baseUrl}}/api/v1/auth/register",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json",
										"type": "text"
									},
									{
										"key": "Authorization",
										"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTc5OTIsInN1YiI6IjgifQ.VRehD9y5dCZkOu8aFBen5x4omrDkcegRcN4NmiGH9JY",
										"type": "text"
									},
									{
										"key": "Accept",
										"value": "application/json",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"email\": \"datauser2@yourorg.com\",\n  \"username\": \"datauser1\",\n  \"password\": \"StrongPassw0rd!\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/auth/register"
							},
							"response": []
						},
						{
							"name": "{{baseUrl}}/api/v1/auth/register-o-convener",
							"request": {
								"auth": {
									"type": "noauth"
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json",
										"type": "text"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "  {\n    \"user_in\": {\n      \"email\": \"demo-11@email.io\",\n      \"username\": \"demouser\",\n      \"password\": \"Pass1234!\",\n      \"permission_level\": 3\n    },\n    \"organization_in\": {\n      \"name\": \"示例组织B\",\n      \"description\": \"这是一个演示用的组织描述。\",\n      \"email_domain\": \"example.demo.org\",\n      \"verification_document\": \"dummy_base64_string_for_test\"\n    }\n  }",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/auth/register-o-convener"
							},
							"response": []
						},
						{
							"name": "{{baseUrl}}/api/v1/auth/register",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json",
										"type": "text"
									},
									{
										"key": "Authorization",
										"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY3MTEzOTEsInN1YiI6IjgifQ.GV0duIaRN0ZY6-8ZbzXw2i4fSA7RbGIXOx31_WnBlds",
										"type": "text"
									},
									{
										"key": "Accept",
										"value": "application/json",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"email\": \"datauser6@yourorg.com\",\n  \"username\": \"datauser1\",\n  \"password\": \"StrongPassw0rd!\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/auth/register"
							},
							"response": []
						}
					]
				},
				{
					"name": "users",
					"item": [
						{
							"name": "me",
							"item": [
								{
									"name": "Read User Me",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": "{{baseUrl}}/api/v1/users/me",
										"description": "获取当前登录用户信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
										},
										{
											"name": "E-admin",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										},
										{
											"name": "Senior-E-admin",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgzNDksInN1YiI6IjYifQ.coJ3eN-HbnS259X-8fTcQl3HjFritA3xBNzLA-m0lvg",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										},
										{
											"name": "O-Convener",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg0ODYsInN1YiI6IjgifQ.o_VpRfrXj8CVNh3H3uWgpijQAUkhzIg-ZY7CQktroNg",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										},
										{
											"name": "T-admin",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Accept",
														"value": "application/json"
													},
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg1NTMsInN1YiI6IjUifQ.ojqhTrunIVvAnJDTx9DJHFtcURdiXaEjCNrjtkGgQKM",
														"type": "text"
													}
												],
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										}
									]
								},
								{
									"name": "Update User Me",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"password\": \"<string>\",\n  \"username\": \"<string>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/users/me",
										"description": "更新当前登录用户信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"password\": \"<string>\",\n  \"username\": \"<string>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"password\": \"<string>\",\n  \"username\": \"<string>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": "{{baseUrl}}/api/v1/users/me"
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "{user_id}",
							"item": [
								{
									"name": "Read User By Id",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/:user_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												":user_id"
											],
											"variable": [
												{
													"key": "user_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取用户信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update User",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"<email>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"password\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"paper_download_quota\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/:user_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												":user_id"
											],
											"variable": [
												{
													"key": "user_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新用户信息（需要E-Admin权限）"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"email\": \"<email>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"password\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"paper_download_quota\": \"<number>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"email\": \"<email>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"password\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"paper_download_quota\": \"<number>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Delete User",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "DELETE",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/:user_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												":user_id"
											],
											"variable": [
												{
													"key": "user_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "删除用户（需要T-Admin权限）"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/users/:user_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"users",
														":user_id"
													],
													"variable": [
														{
															"key": "user_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Users",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"users",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取用户列表（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"email\": \"<email>\",\n    \"id\": \"<integer>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"paper_download_quota\": \"<number>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\",\n    \"organization_id\": \"<integer>\"\n  },\n  {\n    \"email\": \"<email>\",\n    \"id\": \"<integer>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"paper_download_quota\": \"<number>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\",\n    \"organization_id\": \"<integer>\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "E-admin Get all users",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "Senior E-admin Get all users",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgzNDksInN1YiI6IjYifQ.coJ3eN-HbnS259X-8fTcQl3HjFritA3xBNzLA-m0lvg",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "T-admin Get all users",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											},
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg1NTMsInN1YiI6IjUifQ.ojqhTrunIVvAnJDTx9DJHFtcURdiXaEjCNrjtkGgQKM",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Create User",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/users/",
								"description": "创建新用户（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/users/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"<email>\",\n  \"password\": \"<string>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/users/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "E-admin",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json",
												"type": "text"
											},
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"email\": \"newdatauser@someorg.com\",\n  \"username\": \"newdatauser\",\n  \"password\": \"StrongPassw0rd!\",\n  \"role\": \"DATA_USER\",\n  \"organization_id\": 5\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/users/"
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Add Paper Download Quota",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"amount\": \"<number>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": {
									"raw": "{{baseUrl}}/api/v1/users/add-quota/:user_id",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"users",
										"add-quota",
										":user_id"
									],
									"variable": [
										{
											"key": "user_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "为用户增加论文下载配额（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/add-quota/:user_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												"add-quota",
												":user_id"
											],
											"variable": [
												{
													"key": "user_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"email\": \"<email>\",\n  \"id\": \"<integer>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"paper_download_quota\": \"<number>\",\n  \"username\": \"<string>\",\n  \"is_active\": \"<boolean>\",\n  \"role\": \"<string>\",\n  \"permission_level\": \"<integer>\",\n  \"organization_id\": \"<integer>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/users/add-quota/:user_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"users",
												"add-quota",
												":user_id"
											],
											"variable": [
												{
													"key": "user_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "{{baseUrl}}/api/v1/users/",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json",
										"type": "text"
									},
									{
										"key": "Authorization",
										"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
										"type": "text"
									},
									{
										"key": "Accept",
										"value": "application/json",
										"type": "text"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"email\": \"newdatauser4@someorg.com\",\n  \"username\": \"newdatauser\",\n  \"password\": \"StrongPassw0rd!\",\n  \"role\": \"SENIOR_E_ADMIN\",\n  \"organization_id\": 5\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/users/"
							},
							"response": []
						}
					]
				},
				{
					"name": "organizations",
					"item": [
						{
							"name": "{organization_id}",
							"item": [
								{
									"name": "Read Organization",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												":organization_id"
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取组织信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"name\": \"<string>\",\n  \"id\": \"<integer>\",\n  \"convener_id\": \"<integer>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update Organization",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"convener_id\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												":organization_id"
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新组织信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"convener_id\": \"<integer>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"name\": \"<string>\",\n  \"id\": \"<integer>\",\n  \"convener_id\": \"<integer>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"convener_id\": \"<integer>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Upload Verification Document",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "multipart/form-data"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "formdata",
											"formdata": [
												{
													"key": "file",
													"description": "(Required) ",
													"type": "file",
													"src": []
												}
											]
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/upload-verification",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												":organization_id",
												"upload-verification"
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "上传组织验证文件"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "formdata",
													"formdata": [
														{
															"key": "file",
															"value": "<binary>",
															"description": "(Required) ",
															"type": "text"
														}
													]
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/upload-verification",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id",
														"upload-verification"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"name\": \"<string>\",\n  \"id\": \"<integer>\",\n  \"convener_id\": \"<integer>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "formdata",
													"formdata": [
														{
															"key": "file",
															"value": "<binary>",
															"description": "(Required) ",
															"type": "text"
														}
													]
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/upload-verification",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id",
														"upload-verification"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Read Organization Members",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/members?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												":organization_id",
												"members"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "获取组织成员列表"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/members?skip=0&limit=100",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id",
														"members"
													],
													"query": [
														{
															"key": "skip",
															"value": "0"
														},
														{
															"key": "limit",
															"value": "100"
														}
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "[\n  {\n    \"email\": \"<email>\",\n    \"id\": \"<integer>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"paper_download_quota\": \"<number>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\",\n    \"organization_id\": \"<integer>\"\n  },\n  {\n    \"email\": \"<email>\",\n    \"id\": \"<integer>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"paper_download_quota\": \"<number>\",\n    \"username\": \"<string>\",\n    \"is_active\": \"<boolean>\",\n    \"role\": \"<string>\",\n    \"permission_level\": \"<integer>\",\n    \"organization_id\": \"<integer>\"\n  }\n]"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/organizations/:organization_id/members?skip=0&limit=100",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"organizations",
														":organization_id",
														"members"
													],
													"query": [
														{
															"key": "skip",
															"value": "0"
														},
														{
															"key": "limit",
															"value": "100"
														}
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Organizations",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/organizations/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"organizations",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取组织列表（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"name\": \"<string>\",\n    \"id\": \"<integer>\",\n    \"convener_id\": \"<integer>\",\n    \"is_verified\": \"<boolean>\",\n    \"is_active\": \"<boolean>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"description\": \"<string>\",\n    \"email_domain\": \"<string>\"\n  },\n  {\n    \"name\": \"<string>\",\n    \"id\": \"<integer>\",\n    \"convener_id\": \"<integer>\",\n    \"is_verified\": \"<boolean>\",\n    \"is_active\": \"<boolean>\",\n    \"created_at\": \"<dateTime>\",\n    \"updated_at\": \"<dateTime>\",\n    \"description\": \"<string>\",\n    \"email_domain\": \"<string>\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "E-admin",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/organizations/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"organizations",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						},
						{
							"name": "Create Organization",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"verification_document\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/organizations/",
								"description": "创建新组织（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"verification_document\": \"<string>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/organizations/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"name\": \"<string>\",\n  \"id\": \"<integer>\",\n  \"convener_id\": \"<integer>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"name\": \"<string>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\",\n  \"verification_document\": \"<string>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/organizations/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Organization",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": "{{baseUrl}}/api/v1/organizations/my-organization",
								"description": "获取当前用户所属组织信息"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": "{{baseUrl}}/api/v1/organizations/my-organization"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"name\": \"<string>\",\n  \"id\": \"<integer>\",\n  \"convener_id\": \"<integer>\",\n  \"is_verified\": \"<boolean>\",\n  \"is_active\": \"<boolean>\",\n  \"created_at\": \"<dateTime>\",\n  \"updated_at\": \"<dateTime>\",\n  \"description\": \"<string>\",\n  \"email_domain\": \"<string>\"\n}"
								}
							]
						}
					]
				},
				{
					"name": "services",
					"item": [
						{
							"name": "{service_id}",
							"item": [
								{
									"name": "Read Service",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/:service_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												":service_id"
											],
											"variable": [
												{
													"key": "service_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取服务信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"non_ea\": 76967785.52572802,\n  \"autef\": \"incididunt sit sint\",\n  \"sit1\": \"tempor officia Lorem\",\n  \"laboris99\": \"ut\",\n  \"sunt_1e\": 53329666.352656424\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update Service",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/:service_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												":service_id"
											],
											"variable": [
												{
													"key": "service_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新服务信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"labore_37\": -26411332.139440805,\n  \"fugiat_b\": \"deserunt ex reprehenderit\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Delete Service",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "DELETE",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/:service_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												":service_id"
											],
											"variable": [
												{
													"key": "service_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "删除服务"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"aute11a\": 10646154.820595741,\n  \"incididunt644\": \"Ut exercitation incididunt\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/services/:service_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"services",
														":service_id"
													],
													"variable": [
														{
															"key": "service_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Services",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/services/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"services",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取服务列表"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"incididunt466\": 86933194.15254784\n  },\n  {\n    \"sunt_69\": \"ipsum sit adipisicing nisi ex\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Create Service",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/services/",
								"description": "创建新服务（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/services/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"ullamcofdf\": -66363906.07705169,\n  \"pariatur_4da\": \"est dolor\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"tempor_6\": false,\n  \"reprehenderit_f\": -45140348\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/services/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Services",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/services/my-services?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"services",
										"my-services"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取当前用户组织的服务列表（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/my-services?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												"my-services"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"mollit93\": false,\n    \"do94\": \"eu\",\n    \"esse_d\": false,\n    \"nostrudb92\": 87737505\n  },\n  {\n    \"deserunte\": 85125102.9350144\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/services/my-services?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"services",
												"my-services"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "papers",
					"item": [
						{
							"name": "{paper_id}",
							"item": [
								{
									"name": "Read Paper",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												":paper_id"
											],
											"variable": [
												{
													"key": "paper_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取论文信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"magna_8e4\": \"Excepteur eu\",\n  \"reprehenderit6_\": 42448211.80336279,\n  \"qui___9\": false\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update Paper",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"title\": \"<string>\",\n  \"authors\": \"<string>\",\n  \"abstract\": \"<string>\",\n  \"keywords\": \"<string>\",\n  \"is_public\": \"<boolean>\",\n  \"download_fee\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												":paper_id"
											],
											"variable": [
												{
													"key": "paper_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新论文信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"title\": \"<string>\",\n  \"authors\": \"<string>\",\n  \"abstract\": \"<string>\",\n  \"keywords\": \"<string>\",\n  \"is_public\": \"<boolean>\",\n  \"download_fee\": \"<number>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"labore291\": 41238821,\n  \"mollit9\": -31998878.10019009,\n  \"inf9_\": false,\n  \"pariatur_a\": true\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"title\": \"<string>\",\n  \"authors\": \"<string>\",\n  \"abstract\": \"<string>\",\n  \"keywords\": \"<string>\",\n  \"is_public\": \"<boolean>\",\n  \"download_fee\": \"<number>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Delete Paper",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "DELETE",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												":paper_id"
											],
											"variable": [
												{
													"key": "paper_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "删除论文"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"quis_d\": -75815745.1563473\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Download Paper",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/:paper_id/download",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												":paper_id",
												"download"
											],
											"variable": [
												{
													"key": "paper_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "下载论文"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id/download",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id",
														"download"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/papers/:paper_id/download",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"papers",
														":paper_id",
														"download"
													],
													"variable": [
														{
															"key": "paper_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Papers",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/papers/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"papers",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取论文列表"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"in_68\": 36805397.49217093\n  },\n  {\n    \"fugiat9\": -66757186.88273001\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Upload Paper",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "multipart/form-data"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "formdata",
									"formdata": [
										{
											"key": "title",
											"value": "<string>",
											"description": "(Required) ",
											"type": "text"
										},
										{
											"key": "authors",
											"value": "<string>",
											"description": "(Required) ",
											"type": "text"
										},
										{
											"key": "file",
											"description": "(Required) ",
											"type": "file",
											"src": []
										},
										{
											"key": "abstract",
											"value": "<string>",
											"type": "text"
										},
										{
											"key": "keywords",
											"value": "<string>",
											"type": "text"
										},
										{
											"key": "is_public",
											"value": "true",
											"type": "text"
										},
										{
											"key": "download_fee",
											"value": "0",
											"type": "text"
										}
									]
								},
								"url": "{{baseUrl}}/api/v1/papers/",
								"description": "上传论文（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "formdata",
											"formdata": [
												{
													"key": "title",
													"value": "<string>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "authors",
													"value": "<string>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "file",
													"value": "<binary>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "abstract",
													"value": "<string>",
													"type": "text"
												},
												{
													"key": "keywords",
													"value": "<string>",
													"type": "text"
												},
												{
													"key": "is_public",
													"value": "true",
													"type": "text"
												},
												{
													"key": "download_fee",
													"value": "0",
													"type": "text"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/papers/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"quis_05\": -68072468,\n  \"proident_17\": \"occaecat officia cupid\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "formdata",
											"formdata": [
												{
													"key": "title",
													"value": "<string>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "authors",
													"value": "<string>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "file",
													"value": "<binary>",
													"description": "(Required) ",
													"type": "text"
												},
												{
													"key": "abstract",
													"value": "<string>",
													"type": "text"
												},
												{
													"key": "keywords",
													"value": "<string>",
													"type": "text"
												},
												{
													"key": "is_public",
													"value": "true",
													"type": "text"
												},
												{
													"key": "download_fee",
													"value": "0",
													"type": "text"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/papers/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Papers",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/papers/my-papers?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"papers",
										"my-papers"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取当前用户组织的论文列表（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/my-papers?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												"my-papers"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"commodo608\": -20176906.2130896,\n    \"laborum_389\": false\n  },\n  {\n    \"Excepteur_\": -3587401.5694713295,\n    \"ullamco6e5\": -29628788,\n    \"nulla_e\": \"consectetur incididunt\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/my-papers?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												"my-papers"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Search Papers",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/papers/search/?keyword=<string>&author=<string>&organization_id=<integer>&skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"papers",
										"search",
										""
									],
									"query": [
										{
											"key": "keyword",
											"value": "<string>",
											"description": "搜索关键词"
										},
										{
											"key": "author",
											"value": "<string>",
											"description": "作者名称"
										},
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "组织ID"
										},
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "搜索论文"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/search/?keyword=<string>&author=<string>&organization_id=<integer>&skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												"search",
												""
											],
											"query": [
												{
													"key": "keyword",
													"value": "<string>"
												},
												{
													"key": "author",
													"value": "<string>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"ullamco_6\": -59982388.71302038\n  },\n  {\n    \"nullae\": -73739367.52568251,\n    \"veniam_5\": 77087849.83551413,\n    \"tempor_9\": \"aute mollit Excepteur qui\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/papers/search/?keyword=<string>&author=<string>&organization_id=<integer>&skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"papers",
												"search",
												""
											],
											"query": [
												{
													"key": "keyword",
													"value": "<string>"
												},
												{
													"key": "author",
													"value": "<string>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "courses",
					"item": [
						{
							"name": "{course_id}",
							"item": [
								{
									"name": "Read Course",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/:course_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												":course_id"
											],
											"variable": [
												{
													"key": "course_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取课程信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"deserunt_b3\": \"aliqua nostrud Excepteur\",\n  \"Lorem7f\": 55730841\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update Course",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/:course_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												":course_id"
											],
											"variable": [
												{
													"key": "course_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新课程信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"sint_73\": true,\n  \"minim_d\": true,\n  \"deserunt4\": false,\n  \"reprehenderit_d\": -40330402\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Delete Course",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "DELETE",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/:course_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												":course_id"
											],
											"variable": [
												{
													"key": "course_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "删除课程"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"proident5\": 956177.3816879243,\n  \"aute1cc\": false\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/courses/:course_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"courses",
														":course_id"
													],
													"variable": [
														{
															"key": "course_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Courses",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/courses/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"courses",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取课程列表"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"in1f\": -8080529,\n    \"qui0\": 34040212\n  },\n  {\n    \"in_6e\": -51952804.602258995,\n    \"reprehenderit_9b\": 83167568.21202481\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Create Course",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/courses/",
								"description": "创建新课程（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/courses/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"aliquip_999\": false,\n  \"enim_c\": \"dolor id consequat sed ex\"\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"Loremc2\": -10572869,\n  \"amet6\": -96490330\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/courses/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Courses",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/courses/my-courses?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"courses",
										"my-courses"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取当前用户组织的课程列表（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/my-courses?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												"my-courses"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"sint_1d0\": 49010566\n  },\n  {\n    \"tempor_54\": 23888538,\n    \"amet_7\": \"aliquip exercitation voluptate\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/my-courses?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												"my-courses"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Search Courses",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/courses/search/?keyword=<string>&instructor=<string>&organization_id=<integer>&skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"courses",
										"search",
										""
									],
									"query": [
										{
											"key": "keyword",
											"value": "<string>",
											"description": "搜索关键词"
										},
										{
											"key": "instructor",
											"value": "<string>",
											"description": "讲师名称"
										},
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "组织ID"
										},
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "搜索课程"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/search/?keyword=<string>&instructor=<string>&organization_id=<integer>&skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												"search",
												""
											],
											"query": [
												{
													"key": "keyword",
													"value": "<string>"
												},
												{
													"key": "instructor",
													"value": "<string>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"elitd54\": \"aliqua labore\",\n    \"dolor_64\": \"Ut consectetur Lorem\",\n    \"Duis12_\": \"ullamco nisi quis\"\n  },\n  {\n    \"labore344\": -10529959,\n    \"nulla_3\": -25282620\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/courses/search/?keyword=<string>&instructor=<string>&organization_id=<integer>&skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"courses",
												"search",
												""
											],
											"query": [
												{
													"key": "keyword",
													"value": "<string>"
												},
												{
													"key": "instructor",
													"value": "<string>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "payments",
					"item": [
						{
							"name": "Read Payments",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/payments/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"payments",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取支付记录列表（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"labore6\": 78833514.42112118,\n    \"et_b9b\": false,\n    \"occaecat__d\": 38144834.80257112,\n    \"inf\": -32505931,\n    \"amet_68\": 52612358\n  },\n  {\n    \"do_5f\": 69654933.73609987,\n    \"commodo21\": true\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Payments",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/payments/my-payments?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"payments",
										"my-payments"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取当前用户的支付记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/my-payments?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												"my-payments"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"consequatca\": -53401755,\n    \"amet_789\": true,\n    \"dolore_3\": false,\n    \"deserunt_ea\": true\n  },\n  {\n    \"ad_0\": \"sed ullamco\",\n    \"fugiat_e1d\": -9872901.371054083,\n    \"officia_0e\": 717941.3550872952\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/my-payments?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												"my-payments"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Organization Payments",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/payments/organization/:organization_id?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"payments",
										"organization",
										":organization_id"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									],
									"variable": [
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "获取组织的支付记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/organization/:organization_id?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"aliquab6\": 76075765.38350856\n  },\n  {\n    \"enim_d00\": -53930028.10208549,\n    \"esse_5\": 33817710,\n    \"exercitation_c7\": -39255212.27283961\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/organization/:organization_id?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Payment",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/payments/:payment_id",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"payments",
										":payment_id"
									],
									"variable": [
										{
											"key": "payment_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "根据ID获取支付记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/:payment_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												":payment_id"
											],
											"variable": [
												{
													"key": "payment_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"elit_6\": -74063939\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/payments/:payment_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"payments",
												":payment_id"
											],
											"variable": [
												{
													"key": "payment_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Recharge Account",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"amount\": \"<number>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/payments/recharge",
								"description": "为当前用户充值下载配额"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/payments/recharge"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"incididunt_14\": -48991547.33167364\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/payments/recharge"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Withdraw Funds",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"amount\": \"<number>\",\n  \"account_id\": \"<integer>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/payments/withdraw",
								"description": "组织提现（需要O-Convener权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\",\n  \"account_id\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/payments/withdraw"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"et1\": true\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"amount\": \"<number>\",\n  \"account_id\": \"<integer>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/payments/withdraw"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "student-verification",
					"item": [
						{
							"name": "Verify Student",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"student_id\": \"<string>\",\n  \"name\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"additional_info\": {\n    \"velita\": -98948310.31284927,\n    \"nostrud8\": 62819420.44035977\n  }\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/student-verification/verify",
								"description": "验证学生身份"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"student_id\": \"<string>\",\n  \"name\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"additional_info\": {\n    \"velita\": -98948310.31284927,\n    \"nostrud8\": 62819420.44035977\n  }\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/student-verification/verify"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"esse_2\": true,\n  \"in_c\": 73095072.53321815\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"student_id\": \"<string>\",\n  \"name\": \"<string>\",\n  \"organization_id\": \"<integer>\",\n  \"additional_info\": {\n    \"velita\": -98948310.31284927,\n    \"nostrud8\": 62819420.44035977\n  }\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/student-verification/verify"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Verification History",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/student-verification/history?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"student-verification",
										"history"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取当前用户的验证历史记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/history?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												"history"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"exercitation0\": 2660239,\n    \"reprehenderitc\": -21338302.455161035,\n    \"est_e\": \"eu occaecat sed\"\n  },\n  {\n    \"Excepteur5\": \"ex amet dolor\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/history?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												"history"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Organization Verifications",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/student-verification/organization/:organization_id?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"student-verification",
										"organization",
										":organization_id"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									],
									"variable": [
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "获取组织的验证记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/organization/:organization_id?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"in494\": 33194635.92128527,\n    \"deserunt0\": -17220523,\n    \"aliquip_6\": true,\n    \"officia_1\": \"exercitation veniam in nisi\"\n  },\n  {\n    \"dolor3a3\": \"com\",\n    \"enim_b\": -43847157,\n    \"doloref\": -48162630\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/organization/:organization_id?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Verification",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/student-verification/:verification_id",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"student-verification",
										":verification_id"
									],
									"variable": [
										{
											"key": "verification_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "根据ID获取验证记录"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/:verification_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												":verification_id"
											],
											"variable": [
												{
													"key": "verification_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"proident_cd\": false\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/student-verification/:verification_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"student-verification",
												":verification_id"
											],
											"variable": [
												{
													"key": "verification_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "logs",
					"item": [
						{
							"name": "Read Logs",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/logs/?skip=0&limit=100&log_type=<string>&user_id=<integer>&organization_id=<integer>&start_date=<string>&end_date=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"logs",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										},
										{
											"key": "log_type",
											"value": "<string>",
											"description": "日志类型"
										},
										{
											"key": "user_id",
											"value": "<integer>",
											"description": "用户ID"
										},
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "组织ID"
										},
										{
											"key": "start_date",
											"value": "<string>",
											"description": "开始日期 (YYYY-MM-DD)"
										},
										{
											"key": "end_date",
											"value": "<string>",
											"description": "结束日期 (YYYY-MM-DD)"
										}
									]
								},
								"description": "获取系统日志（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/?skip=0&limit=100&log_type=<string>&user_id=<integer>&organization_id=<integer>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "user_id",
													"value": "<integer>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"id_e80\": true\n  },\n  {\n    \"id_bc3\": true\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/?skip=0&limit=100&log_type=<string>&user_id=<integer>&organization_id=<integer>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "user_id",
													"value": "<integer>"
												},
												{
													"key": "organization_id",
													"value": "<integer>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read My Logs",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/logs/my-logs?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"logs",
										"my-logs"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										},
										{
											"key": "log_type",
											"value": "<string>",
											"description": "日志类型"
										},
										{
											"key": "start_date",
											"value": "<string>",
											"description": "开始日期 (YYYY-MM-DD)"
										},
										{
											"key": "end_date",
											"value": "<string>",
											"description": "结束日期 (YYYY-MM-DD)"
										}
									]
								},
								"description": "获取当前用户的日志"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/my-logs?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												"my-logs"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"Excepteur_9\": -37377317,\n    \"voluptate_1\": false\n  },\n  {\n    \"nulla_b\": -31463891,\n    \"nulla_a4\": -62767280.714056864,\n    \"dolor_14f\": true\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/my-logs?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												"my-logs"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Read Organization Logs",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/logs/organization/:organization_id?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"logs",
										"organization",
										":organization_id"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										},
										{
											"key": "log_type",
											"value": "<string>",
											"description": "日志类型"
										},
										{
											"key": "start_date",
											"value": "<string>",
											"description": "开始日期 (YYYY-MM-DD)"
										},
										{
											"key": "end_date",
											"value": "<string>",
											"description": "结束日期 (YYYY-MM-DD)"
										}
									],
									"variable": [
										{
											"key": "organization_id",
											"value": "<integer>",
											"description": "(Required) "
										}
									]
								},
								"description": "获取组织的日志"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/organization/:organization_id?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"cillum_2\": false,\n    \"aliquip_cf4\": \"esse aute aliquip in\"\n  },\n  {\n    \"enima0\": \"nulla Lorem ut ipsum\",\n    \"dolor88a\": -1601943,\n    \"et2\": false,\n    \"cupidatatcd\": 85027605,\n    \"nostrud8\": -9390783.573890224\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/logs/organization/:organization_id?skip=0&limit=100&log_type=<string>&start_date=<string>&end_date=<string>",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"logs",
												"organization",
												":organization_id"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												},
												{
													"key": "log_type",
													"value": "<string>"
												},
												{
													"key": "start_date",
													"value": "<string>"
												},
												{
													"key": "end_date",
													"value": "<string>"
												}
											],
											"variable": [
												{
													"key": "organization_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "policies",
					"item": [
						{
							"name": "{policy_id}",
							"item": [
								{
									"name": "Read Policy",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"policies",
												":policy_id"
											],
											"variable": [
												{
													"key": "policy_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "根据ID获取政策信息"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"consectetur1\": false,\n  \"nisi_6\": \"esse consequat tempor dolor aute\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Update Policy",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "PUT",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"title\": \"<string>\",\n  \"description\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"is_active\": \"<boolean>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": {
											"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"policies",
												":policy_id"
											],
											"variable": [
												{
													"key": "policy_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "更新政策信息（需要E-Admin权限）"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"title\": \"<string>\",\n  \"description\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"is_active\": \"<boolean>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"ut_c\": -39062441,\n  \"tempor4b9\": 65400435\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "PUT",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"title\": \"<string>\",\n  \"description\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"is_active\": \"<boolean>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								},
								{
									"name": "Delete Policy",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "DELETE",
										"header": [
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"policies",
												":policy_id"
											],
											"variable": [
												{
													"key": "policy_id",
													"value": "<integer>",
													"description": "(Required) "
												}
											]
										},
										"description": "删除政策（需要E-Admin权限）"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"adipisicing_2a\": -90028168\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "DELETE",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/policies/:policy_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"policies",
														":policy_id"
													],
													"variable": [
														{
															"key": "policy_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										}
									]
								}
							]
						},
						{
							"name": "Read Policies",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/policies/?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"policies",
										""
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取政策列表"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/policies/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"policies",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"dolor0\": \"est elit eu reprehenderit\"\n  },\n  {\n    \"dolor9\": false\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/policies/?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"policies",
												""
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Create Policy",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"title\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"description\": \"<string>\"\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/policies/",
								"description": "创建新政策（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"title\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"description\": \"<string>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/policies/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"laboris_8\": 90579980.0397523,\n  \"nostrud_a7\": true,\n  \"nostrudacf\": false,\n  \"laborum_d\": -63687979\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"title\": \"<string>\",\n  \"file_path\": \"<string>\",\n  \"description\": \"<string>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/policies/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Upload Policy File",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "multipart/form-data"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "formdata",
									"formdata": [
										{
											"key": "file",
											"description": "(Required) ",
											"type": "file",
											"src": []
										}
									]
								},
								"url": "{{baseUrl}}/api/v1/policies/upload",
								"description": "上传政策文件（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "formdata",
											"formdata": [
												{
													"key": "file",
													"value": "<binary>",
													"description": "(Required) ",
													"type": "text"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/policies/upload"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"fugiat_7\": -73283937.46224383\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "formdata",
											"formdata": [
												{
													"key": "file",
													"value": "<binary>",
													"description": "(Required) ",
													"type": "text"
												}
											]
										},
										"url": "{{baseUrl}}/api/v1/policies/upload"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "system-config",
					"item": [
						{
							"name": "Get System Config",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"url": "{{baseUrl}}/api/v1/system-config/",
								"description": "获取系统配置"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": "{{baseUrl}}/api/v1/system-config/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"Duis_1a\": -61348193.55992107\n}"
								}
							]
						},
						{
							"name": "Update System Config",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "PUT",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "{\n  \"sint3d3\": 45810801.68536943,\n  \"dolor912\": -15091097\n}",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/system-config/",
								"description": "更新系统配置（需要Senior-E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "PUT",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"sint3d3\": 45810801.68536943,\n  \"dolor912\": -15091097\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/system-config/"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"pariatur_3\": \"cons\",\n  \"culpa_b81\": -28960763.80508825\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "PUT",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"sint3d3\": 45810801.68536943,\n  \"dolor912\": -15091097\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/system-config/"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						},
						{
							"name": "Toggle Maintenance Mode",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "POST",
								"header": [
									{
										"key": "Content-Type",
										"value": "application/json"
									},
									{
										"key": "Accept",
										"value": "application/json"
									}
								],
								"body": {
									"mode": "raw",
									"raw": "<boolean>",
									"options": {
										"raw": {
											"language": "json"
										}
									}
								},
								"url": "{{baseUrl}}/api/v1/system-config/maintenance-mode",
								"description": "切换系统维护模式（需要Senior-E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "<boolean>",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/system-config/maintenance-mode"
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"enim4_b\": -61559710,\n  \"et_f0\": \"non Ut ut incididunt\",\n  \"laboris_bd\": 62259972,\n  \"Lorem8f\": -49517268\n}"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "POST",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "<boolean>",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/system-config/maintenance-mode"
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								}
							]
						}
					]
				},
				{
					"name": "verification",
					"item": [
						{
							"name": "{organization_id}",
							"item": [
								{
									"name": "Get Verification Status",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}",
										"description": "获取组织的验证状态"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/verification/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"verification",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"organization_id\": \"<integer>\",\n  \"id\": \"<integer>\",\n  \"submitted_at\": \"<dateTime>\",\n  \"e_admin_approved\": \"<boolean>\",\n  \"senior_approved\": \"<boolean>\",\n  \"e_admin_comment\": \"<string>\",\n  \"senior_comment\": \"<string>\",\n  \"e_admin_id\": \"<integer>\",\n  \"senior_e_admin_id\": \"<integer>\",\n  \"e_admin_reviewed_at\": \"<dateTime>\",\n  \"senior_reviewed_at\": \"<dateTime>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"url": {
													"raw": "{{baseUrl}}/api/v1/verification/:organization_id",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"verification",
														":organization_id"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										},
										{
											"name": "E-admin Get Verification Status",
											"originalRequest": {
												"method": "GET",
												"header": [
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										}
									]
								},
								{
									"name": "Review Verification",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "POST",
										"header": [
											{
												"key": "Content-Type",
												"value": "application/json"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"body": {
											"mode": "raw",
											"raw": "{\n  \"e_admin_id\": \"<integer>\",\n  \"senior_e_admin_id\": \"<integer>\",\n  \"e_admin_approved\": \"<boolean>\",\n  \"senior_approved\": \"<boolean>\",\n  \"e_admin_comment\": \"<string>\",\n  \"senior_comment\": \"<string>\",\n  \"e_admin_reviewed_at\": \"<dateTime>\",\n  \"senior_reviewed_at\": \"<dateTime>\"\n}",
											"options": {
												"raw": {
													"language": "json"
												}
											}
										},
										"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}/review",
										"description": "审核组织验证申请"
									},
									"response": [
										{
											"name": "Successful Response",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"e_admin_id\": \"<integer>\",\n  \"senior_e_admin_id\": \"<integer>\",\n  \"e_admin_approved\": \"<boolean>\",\n  \"senior_approved\": \"<boolean>\",\n  \"e_admin_comment\": \"<string>\",\n  \"senior_comment\": \"<string>\",\n  \"e_admin_reviewed_at\": \"<dateTime>\",\n  \"senior_reviewed_at\": \"<dateTime>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/verification/:organization_id/review",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"verification",
														":organization_id",
														"review"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "OK",
											"code": 200,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"organization_id\": \"<integer>\",\n  \"id\": \"<integer>\",\n  \"submitted_at\": \"<dateTime>\",\n  \"e_admin_approved\": \"<boolean>\",\n  \"senior_approved\": \"<boolean>\",\n  \"e_admin_comment\": \"<string>\",\n  \"senior_comment\": \"<string>\",\n  \"e_admin_id\": \"<integer>\",\n  \"senior_e_admin_id\": \"<integer>\",\n  \"e_admin_reviewed_at\": \"<dateTime>\",\n  \"senior_reviewed_at\": \"<dateTime>\"\n}"
										},
										{
											"name": "Validation Error",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Authorization",
														"value": "<token>",
														"description": "Added as a part of security scheme: oauth2"
													},
													{
														"key": "Accept",
														"value": "application/json"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"e_admin_id\": \"<integer>\",\n  \"senior_e_admin_id\": \"<integer>\",\n  \"e_admin_approved\": \"<boolean>\",\n  \"senior_approved\": \"<boolean>\",\n  \"e_admin_comment\": \"<string>\",\n  \"senior_comment\": \"<string>\",\n  \"e_admin_reviewed_at\": \"<dateTime>\",\n  \"senior_reviewed_at\": \"<dateTime>\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": {
													"raw": "{{baseUrl}}/api/v1/verification/:organization_id/review",
													"host": [
														"{{baseUrl}}"
													],
													"path": [
														"api",
														"v1",
														"verification",
														":organization_id",
														"review"
													],
													"variable": [
														{
															"key": "organization_id",
															"value": "<integer>",
															"description": "(Required) "
														}
													]
												}
											},
											"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
											"code": 422,
											"_postman_previewlanguage": "json",
											"header": [
												{
													"key": "Content-Type",
													"value": "application/json"
												}
											],
											"cookie": [],
											"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
										},
										{
											"name": "E-admin Review",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Content-Type",
														"value": "application/json",
														"type": "text"
													},
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"e_admin_approved\": true,\n  \"e_admin_comment\": \"材料齐全，符合要求。\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}/review"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										},
										{
											"name": "Senior E-admin Review",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Content-Type",
														"value": "application/json",
														"type": "text"
													},
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg1NTMsInN1YiI6IjUifQ.ojqhTrunIVvAnJDTx9DJHFtcURdiXaEjCNrjtkGgQKM",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n  \"t_admin_approved\": true,\n  \"t_admin_comment\": \"符合要求\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}/review"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										},
										{
											"name": "T-admin Review",
											"originalRequest": {
												"method": "POST",
												"header": [
													{
														"key": "Content-Type",
														"value": "application/json",
														"type": "text"
													},
													{
														"key": "Accept",
														"value": "application/json",
														"type": "text"
													},
													{
														"key": "Authorization",
														"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg1NTMsInN1YiI6IjUifQ.ojqhTrunIVvAnJDTx9DJHFtcURdiXaEjCNrjtkGgQKM",
														"type": "text"
													}
												],
												"body": {
													"mode": "raw",
													"raw": "{\n    \"e_admin_approved\": true,\n    \"e_admin_comment\": \"技术管理员初审通过\",\n    \"senior_approved\": true,\n    \"senior_comment\": \"技术管理员终审通过\"\n}",
													"options": {
														"raw": {
															"language": "json"
														}
													}
												},
												"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}/review"
											},
											"_postman_previewlanguage": null,
											"header": null,
											"cookie": [],
											"body": null
										}
									]
								},
								{
									"name": "{{baseUrl}}/api/v1/verification/{{organization_id}}",
									"request": {
										"auth": {
											"type": "oauth2",
											"oauth2": {
												"accessTokenUrl": "/api/v1/auth/login",
												"grant_type": "password_credentials"
											}
										},
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": "{{baseUrl}}/api/v1/verification/{{organization_id}}"
									},
									"response": []
								}
							],
							"auth": {
								"type": "oauth2",
								"oauth2": {
									"addTokenTo": "header"
								}
							},
							"event": [
								{
									"listen": "prerequest",
									"script": {
										"type": "text/javascript",
										"packages": {},
										"exec": [
											""
										]
									}
								},
								{
									"listen": "test",
									"script": {
										"type": "text/javascript",
										"packages": {},
										"exec": [
											""
										]
									}
								}
							]
						},
						{
							"name": "Get Pending Verifications",
							"request": {
								"auth": {
									"type": "oauth2",
									"oauth2": {
										"accessTokenUrl": "/api/v1/auth/login",
										"grant_type": "password_credentials"
									}
								},
								"method": "GET",
								"header": [
									{
										"key": "Authorization",
										"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
										"type": "text"
									},
									{
										"key": "Accept",
										"value": "application/json",
										"type": "text"
									}
								],
								"url": {
									"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
									"host": [
										"{{baseUrl}}"
									],
									"path": [
										"api",
										"v1",
										"verification",
										"pending"
									],
									"query": [
										{
											"key": "skip",
											"value": "0"
										},
										{
											"key": "limit",
											"value": "100"
										}
									]
								},
								"description": "获取待审核的组织验证申请列表（需要E-Admin权限）"
							},
							"response": [
								{
									"name": "Successful Response",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"verification",
												"pending"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "OK",
									"code": 200,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "[\n  {\n    \"organization_id\": \"<integer>\",\n    \"id\": \"<integer>\",\n    \"submitted_at\": \"<dateTime>\",\n    \"e_admin_approved\": \"<boolean>\",\n    \"senior_approved\": \"<boolean>\",\n    \"e_admin_comment\": \"<string>\",\n    \"senior_comment\": \"<string>\",\n    \"e_admin_id\": \"<integer>\",\n    \"senior_e_admin_id\": \"<integer>\",\n    \"e_admin_reviewed_at\": \"<dateTime>\",\n    \"senior_reviewed_at\": \"<dateTime>\"\n  },\n  {\n    \"organization_id\": \"<integer>\",\n    \"id\": \"<integer>\",\n    \"submitted_at\": \"<dateTime>\",\n    \"e_admin_approved\": \"<boolean>\",\n    \"senior_approved\": \"<boolean>\",\n    \"e_admin_comment\": \"<string>\",\n    \"senior_comment\": \"<string>\",\n    \"e_admin_id\": \"<integer>\",\n    \"senior_e_admin_id\": \"<integer>\",\n    \"e_admin_reviewed_at\": \"<dateTime>\",\n    \"senior_reviewed_at\": \"<dateTime>\"\n  }\n]"
								},
								{
									"name": "Validation Error",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "<token>",
												"description": "Added as a part of security scheme: oauth2"
											},
											{
												"key": "Accept",
												"value": "application/json"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"verification",
												"pending"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"status": "Unprocessable Entity (WebDAV) (RFC 4918)",
									"code": 422,
									"_postman_previewlanguage": "json",
									"header": [
										{
											"key": "Content-Type",
											"value": "application/json"
										}
									],
									"cookie": [],
									"body": "{\n  \"detail\": [\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    },\n    {\n      \"loc\": [\n        \"<string>\",\n        \"<string>\"\n      ],\n      \"msg\": \"<string>\",\n      \"type\": \"<string>\"\n    }\n  ]\n}"
								},
								{
									"name": "E-Admin",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgxNzcsInN1YiI6IjcifQ.X7R8DFqqJ60bcPpEvXlFHqxLHLl5j4f1O3V9XCm5lcc",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"verification",
												"pending"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "Senior E-admin",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTgzNDksInN1YiI6IjYifQ.coJ3eN-HbnS259X-8fTcQl3HjFritA3xBNzLA-m0lvg",
												"type": "text"
											},
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"verification",
												"pending"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								},
								{
									"name": "T-admin",
									"originalRequest": {
										"method": "GET",
										"header": [
											{
												"key": "Accept",
												"value": "application/json",
												"type": "text"
											},
											{
												"key": "Authorization",
												"value": "bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDY2OTg1NTMsInN1YiI6IjUifQ.ojqhTrunIVvAnJDTx9DJHFtcURdiXaEjCNrjtkGgQKM",
												"type": "text"
											}
										],
										"url": {
											"raw": "{{baseUrl}}/api/v1/verification/pending?skip=0&limit=100",
											"host": [
												"{{baseUrl}}"
											],
											"path": [
												"api",
												"v1",
												"verification",
												"pending"
											],
											"query": [
												{
													"key": "skip",
													"value": "0"
												},
												{
													"key": "limit",
													"value": "100"
												}
											]
										}
									},
									"_postman_previewlanguage": null,
									"header": null,
									"cookie": [],
									"body": null
								}
							]
						}
					]
				}
			]
		},
		{
			"name": "Root",
			"request": {
				"method": "GET",
				"header": [
					{
						"key": "Accept",
						"value": "application/json"
					}
				],
				"url": "{{baseUrl}}/"
			},
			"response": [
				{
					"name": "Successful Response",
					"originalRequest": {
						"method": "GET",
						"header": [
							{
								"key": "Accept",
								"value": "application/json"
							}
						],
						"url": "{{baseUrl}}/"
					},
					"status": "OK",
					"code": 200,
					"_postman_previewlanguage": "json",
					"header": [
						{
							"key": "Content-Type",
							"value": "application/json"
						}
					],
					"cookie": [],
					"body": "{}"
				}
			]
		}
	],
	"event": [
		{
			"listen": "prerequest",
			"script": {
				"type": "text/javascript",
				"packages": {},
				"exec": [
					""
				]
			}
		},
		{
			"listen": "test",
			"script": {
				"type": "text/javascript",
				"packages": {},
				"exec": [
					""
				]
			}
		}
	],
	"variable": [
		{
			"key": "baseUrl",
			"value": "/",
			"type": "string"
		},
		{
			"key": "organization_id",
			"value": "",
			"type": "default"
		}
	]
}
```