import { rest } from 'msw'
import { setupWorker } from 'msw'

// Add base URL to all handlers
const BASE_URL = 'http://localhost:8000'

export const setupMockServer = () => {
  const worker = setupWorker(
    // Update login handler with full URL
    rest.post(`${BASE_URL}/api/v1/auth/login`, (req, res, ctx) => {
      return res(
        ctx.json({
          access_token: 'mocked_access_token',
          token_type: 'Bearer'
        })
      );
    }),
    rest.post('/api/v1/students/verify', (req, res, ctx) => {
      const { name, student_id, school } = req.body;
      return res(
        ctx.json({
          verified: true,
          student: {
            name,
            student_id,
            school,
            status: 'Enrolled',
            major: 'Computer Science and Technology',
            enrollment_year: '2020'
          }
        })
      );
    }),

    // 批量学生身份验证接口
    rest.post('/api/v1/students/verify/batch', async (req, res, ctx) => {
      // 模拟文件处理
      return res(
        ctx.json({
          total: 2,
          success: 2,
          failed: 0,
          results: [
            {
              name: 'Zhang San',
              student_id: '2020001',
              school: 'Example University',
              verified: true,
              status: 'Enrolled'
            },
            {
              name: 'Li Si',
              student_id: '2020002',
              school: 'Example University',
              verified: true,
              status: 'Enrolled'
            }
          ]
        })
      );
    }),

    // GPA记录查询接口
    rest.post('/api/v1/students/gpa', (req, res, ctx) => {
      const { name, student_id, school } = req.body;
      return res(
        ctx.json({
          student: {
            name,
            student_id,
            school,
            major: 'Computer Science and Technology'
          },
          gpa_records: [
            {
              semester: '2020-2021-1',
              gpa: 3.8,
              credits: 24,
              courses: [
                { name: '高等数学', credit: 4, grade: 'A' },
                { name: '程序设计基础', credit: 3, grade: 'A' }
              ]
            },
            {
              semester: '2020-2021-2',
              gpa: 3.9,
              credits: 26,
              courses: [
                { name: '数据结构', credit: 4, grade: 'A' },
                { name: '计算机网络', credit: 3, grade: 'A' }
              ]
            }
          ]
        })
      );
    }),
    rest.get('/api/v1/users', (req, res, ctx) => {
      return res(
        ctx.json({
          users: [
            { id: 1, name: 'John Doe' },
            { id: 2, name: 'Jane Doe' }
          ]
        })
      );
    }),
    rest.post('/api/v1/auth/register', (req, res, ctx) => {
      return res(
        ctx.json({
          email: req.body.email,
          id: 123,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          paper_download_quota: 10,
          username: req.body.username,
          is_active: true,
          role: req.body.role,
          permission_level: req.body.permission_level,
          organization_id: 1
        })
      );
    }),

    // 课程列表接口
    rest.get('/api/v1/courses', (req, res, ctx) => {
      const { page = 1, page_size = 10, keyword } = req.url.searchParams;
      const filtered = mockCourses
        .filter(course => 
          !keyword || 
          course.name.includes(keyword) || 
          course.instructor.includes(keyword)
        )
      return res(
        ctx.json({
          total: filtered.length,
          items: filtered.slice((page-1)*page_size, page*page_size)
        })
      );
    }),

    // 课程详情接口
    rest.get('/api/v1/courses/:id', (req, res, ctx) => {
      const course = mockCourses.find(c => c.id === req.params.id);
      return course 
        ? res(ctx.json(course))
        : res(ctx.status(404));
    }),

    // 课程搜索接口
    rest.get('/api/v1/courses/search', (req, res, ctx) => {
      const { q, page = 1, page_size = 10 } = req.url.searchParams;
      const results = mockCourses
        .filter(course => 
          course.name.includes(q) ||
          course.description.includes(q) ||
          course.instructor.includes(q)
        )
      return res(
        ctx.json({
          total: results.length,
          items: results.slice((page-1)*page_size, page*page_size)
        })
      );
    }),

    // 课程创建接口
    rest.post('/api/v1/courses', (req, res, ctx) => {
      const courseData = req.body;
      if (!courseData.name || !courseData.instructor || !courseData.credit) {
        return res(ctx.status(400), ctx.json({ error: 'Missing required fields' }));
      }
      const newCourse = {
        id: `CS${mockCourses.length.toString().padStart(4, '0')}`,
        ...courseData,
        syllabus: courseData.syllabus || [],
        textbooks: courseData.textbooks || [],
        department: courseData.department || 'School of Computer Science',
        academic_year: courseData.academic_year || '2023-2024'
      };
      mockCourses.push(newCourse);
      return res(ctx.json(newCourse));
    }),

    // 课程更新接口
    rest.put('/api/v1/courses/:id', (req, res, ctx) => {
      const index = mockCourses.findIndex(c => c.id === req.params.id);
      if (index === -1) return res(ctx.status(404));
      const updates = req.body;
      mockCourses[index] = { ...mockCourses[index], ...updates };
      return res(ctx.json(mockCourses[index]));
    }),

    // 课程删除接口
    rest.delete('/api/v1/courses/:id', (req, res, ctx) => {
      const index = mockCourses.findIndex(c => c.id === req.params.id);
      if (index === -1) return res(ctx.status(404));
      mockCourses.splice(index, 1);
      return res(ctx.json({ success: true }));
    })
  );

  // Add error handling
  worker.start({
    onUnhandledRequest: 'bypass',
    serviceWorker: {
      url: '/mockServiceWorker.js'
    }
  }).catch(error => {
    console.error('MSW worker registration failed:', error)
  })
};

const mockCourses = Array.from({ length: 50 }, (_, i) => ({
  id: `CS${i.toString().padStart(4, '0')}`,
  name: `Computer Science ${i + 1}`, 
  credit: 3 + (i % 3),
  instructor: `Professor ${String.fromCharCode(65 + (i % 26))}`,
  description: 'Core computer science course covering programming fundamentals, algorithm design and analysis',
  syllabus: Array.from({ length: 15 }, (_, w) => ({
    week: w + 1,
    topic: `Week ${w + 1} Topic`, 
    content: `Week ${w + 1} Course Content Details`
  })),
  schedule: `${i % 4 + 1}-${i % 5 + 101} Classroom`, 
  department: 'School of Computer Science',
  academic_year: '2023-2024'
}));