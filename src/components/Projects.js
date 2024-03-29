import React from "react";

const Projects = () => {
  return (
    <section id="project" className="p-12">
      <div className="max-w-5xl mx-auto px-4">
        <h2 className="text-4xl font-bold text-center mb-10">PROJECTS</h2>
        <div className="flex flex-wrap justify-center items-stretch gap-8">
          <ProjectItem
            title="수길이네 금융마을"
            description="금융 퀴즈/ 카드 뉴스/ 금융 꿀팁을 통해 누구나 즐겁게 금융에 대해 배울수 있는 웹 페이지"
            roles={[
              "회원가입, 로그인 등 유저 정보 관리",
              "커뮤니티 게시판 기능",
              "카카오 맵 은행 검색 기능",
              "금융 꿀팁 및 금융 퀴즈 기능",
            ]}
            techStack={["Vue.js", "Django", "SQLite3"]}
            link="https://github.com/Jonggil-dev/finalpjt_semester1"
          />
          <ProjectItem
            title="눈 깜빡할 새"
            description="WebRTC기술을 활용한 온라인 눈(eye) 싸움 게임"
            roles={[
              "디자인 (피그마 UI/UX 설계)",
              "회원가입, 로그인 등 유저 정보 관리",
              "Jwt Token 등 유저 권한 관리",
              "WebSocket을 통한 실시간 통신",
            ]}
            techStack={[
              "Node.js",
              "React",
              "Spring Boot",
              "OpenVidu",
              "MySql",
              "Redis",
              "AWS",
              "Docker",
            ]}
            link="https://github.com/Jonggil-dev/Staring-Contest"
          />
        </div>
      </div>
    </section>
  );
};

function ProjectItem({ title, description, roles, techStack, link }) {
  return (
    <div className="max-w-md w-full bg-white shadow-lg rounded-lg transition duration-300 ease-in-out hover:scale-105 hover:shadow-xln">
      <div className="p-5">
        <h3 className="text-xl font-semibold mb-3">{title}</h3>
        <div className="text-gray-800">
          <p className="font-medium mb-2">1. 개요:</p>
          <p className="ml-4">· {description}</p>

          <p className="font-medium mt-4 mb-2">2. 역할:</p>
          {roles.map((role, index) => (
            <p key={index} className="ml-4 mb-1">
              · {role}
            </p>
          ))}

          <p className="font-medium mt-4 mb-2">3. 기술스택:</p>
          <div className="flex flex-wrap gap-2 mt-2 ml-4">
            {techStack.map((tech, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
              >
                {tech}
              </span>
            ))}
          </div>

          <p className="font-medium mt-4 mb-2">4. 링크:</p>
          <a
            href={link}
            className="ml-4 text-blue-500 hover:text-blue-600 underline"
          >
            프로젝트 보러가기
          </a>
        </div>
      </div>
    </div>
  );
}

export default Projects;
